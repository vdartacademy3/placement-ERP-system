from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum
from .models import Book, IssuedBook
from .serializers import BookSerializer, IssuedBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search", "")
        category = self.request.query_params.get("category", "")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )
        if category:
            qs = qs.filter(category=category)
        return qs

    def perform_create(self, serializer):
        # On creation available = copies; location_code is set by model.save()
        copies = serializer.validated_data.get("copies", 1)
        serializer.save(available=copies)


class IssuedBookViewSet(viewsets.ModelViewSet):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get("status", "")
        student_id = self.request.query_params.get("student_id", "")
        if status_filter:
            qs = qs.filter(status=status_filter)
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs

    def perform_create(self, serializer):
        issued = serializer.save()
        book = issued.book
        if book.available > 0:
            book.available -= 1
            book.save(update_fields=["available"])

    def perform_update(self, serializer):
        # Capture old status BEFORE saving
        old_status = serializer.instance.status
        issued = serializer.save()
        if old_status != "Returned" and issued.status == "Returned":
            book = issued.book
            book.available = min(book.available + 1, book.copies)
            book.save(update_fields=["available"])

    @action(detail=False, methods=["get"])
    def stats(self, request):
        total_issued    = IssuedBook.objects.filter(status="Issued").count()
        total_overdue   = IssuedBook.objects.filter(status="Overdue").count()
        total_fine      = IssuedBook.objects.aggregate(total=Sum("fine"))["total"] or 0
        total_copies    = Book.objects.aggregate(total=Sum("copies"))["total"] or 0
        total_available = Book.objects.aggregate(total=Sum("available"))["total"] or 0
        return Response({
            "total_copies":    total_copies,
            "total_available": total_available,
            "issued":          total_issued,
            "overdue":         total_overdue,
            "total_fine":      float(total_fine),
        })
