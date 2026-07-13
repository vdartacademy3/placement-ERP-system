from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset         = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=['get'], url_path='stats')
    def stats(self, request, pk=None):
        dept = self.get_object()
        data = {
            'department'    : dept.name,
            'total_faculty' : dept.faculty_members.count(),
            'active_faculty': dept.faculty_members.filter(
                                is_active=True).count(),
            'available_now' : dept.faculty_members.filter(
                                status='available').count(),
            'on_leave'      : dept.faculty_members.filter(
                                status='on_leave').count(),
            'hod'           : dept.faculty_members.filter(
                                is_hod=True
                              ).first().name if dept.faculty_members.filter(
                                is_hod=True).exists() else 'Not assigned',
        }
        return Response(data, status=status.HTTP_200_OK)