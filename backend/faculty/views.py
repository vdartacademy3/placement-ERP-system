from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Faculty
from .serializers import FacultySerializer

class FacultyViewSet(viewsets.ModelViewSet):
    queryset         = Faculty.objects.all()
    serializer_class = FacultySerializer

    def get_queryset(self):
        qs   = super().get_queryset()
        dept = self.request.query_params.get('department')
        stat = self.request.query_params.get('status')
        if dept:
            qs = qs.filter(department_id=dept)
        if stat:
            qs = qs.filter(status=stat)
        return qs

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        faculty         = self.get_object()
        faculty.status  = request.data.get('status', faculty.status)
        faculty.room_no = request.data.get('room_no', faculty.room_no)
        faculty.block   = request.data.get('block', faculty.block)
        faculty.save()
        return Response(
            FacultySerializer(faculty).data,
            status=status.HTTP_200_OK
        ) 