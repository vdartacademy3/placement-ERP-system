from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .models import Student, StudentDocument
from .serializers import (
    StudentSerializer,
    StudentListSerializer,
    StudentDocumentSerializer,
    StudentDashboardSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    Handles all Student CRUD operations.
    GET    /api/students/          -> list with search, filter, pagination
    POST   /api/students/          -> create new student
    GET    /api/students/<id>/     -> retrieve student profile
    PUT    /api/students/<id>/     -> full update
    PATCH  /api/students/<id>/     -> partial update
    DELETE /api/students/<id>/     -> delete student
    GET    /api/students/<id>/profile/   -> student profile with documents
    """
    queryset = Student.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields   = ['first_name', 'last_name', 'email', 'roll_number', 'department']
    filterset_fields = ['department', 'status', 'year_of_study', 'gender']
    ordering_fields  = ['created_at', 'first_name', 'roll_number']
    ordering         = ['-created_at']

    def get_serializer_class(self):
        """Use lightweight serializer for list, full serializer for everything else"""
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(
                {'message': 'Student registered successfully.', 'data': StudentSerializer(student).data},
                status=status.HTTP_201_CREATED
            )
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            student = serializer.save()
            return Response(
                {'message': 'Student updated successfully.', 'data': StudentSerializer(student).data}
            )
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.full_name
        instance.delete()
        return Response({'message': f'Student {name} deleted successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='profile')
    def profile(self, request, pk=None):
        """GET /api/students/<id>/profile/ — full profile with documents"""
        student = self.get_object()
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data)


class StudentDashboardView(APIView):
    """
    GET /api/students/dashboard/
    Returns overall student statistics for the dashboard.
    """
    def get(self, request):
        students = Student.objects.all()

        # Count by status
        status_counts = students.values('status').annotate(count=Count('id'))
        counts = {item['status']: item['count'] for item in status_counts}

        # Department breakdown
        departments = list(
            students.values('department').annotate(count=Count('id')).order_by('department')
        )

        data = {
            'total_students':     students.count(),
            'active_students':    counts.get('active', 0),
            'inactive_students':  counts.get('inactive', 0),
            'graduated_students': counts.get('graduated', 0),
            'departments':        departments,
        }
        serializer = StudentDashboardSerializer(data)
        return Response(serializer.data)


class StudentDocumentView(APIView):
    """
    GET  /api/students/<student_id>/documents/        -> list all documents
    POST /api/students/<student_id>/documents/upload/ -> upload a document
    """
    parser_classes = [MultiPartParser, FormParser]

    def get_student(self, student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return None

    def get(self, request, student_id):
        """List all documents for a student"""
        student = self.get_student(student_id)
        if not student:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        documents = student.documents.all()
        serializer = StudentDocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, student_id):
        """Upload a document for a student"""
        student = self.get_student(student_id)
        if not student:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student)
            return Response(
                {'message': 'Document uploaded successfully.', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StudentDocumentDeleteView(APIView):
    """
    DELETE /api/students/documents/<doc_id>/ -> delete a specific document
    """
    def delete(self, request, doc_id):
        try:
            document = StudentDocument.objects.get(id=doc_id)
        except StudentDocument.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        document.file.delete(save=False)  # delete file from disk
        document.delete()
        return Response({'message': 'Document deleted successfully.'}, status=status.HTTP_200_OK)
