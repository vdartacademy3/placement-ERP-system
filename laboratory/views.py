from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lab, Equipment, Maintenance
from .serializers import LabSerializer, LabDetailSerializer, EquipmentSerializer, MaintenanceSerializer


class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'status', 'lab_type']
    search_fields    = ['name', 'lab_code', 'department']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LabDetailSerializer
        return LabSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_eq     = Equipment.objects.count()
        available_eq = Equipment.objects.filter(status='available').count()
        maintenance_eq = Equipment.objects.filter(status='maintenance').count()
        return Response({
            'total_labs':        Lab.objects.count(),
            'active_labs':       Lab.objects.filter(status='active').count(),
            'total_equipment':   total_eq,
            'available_equipment': available_eq,
            'maintenance_equipment': maintenance_eq,
        })


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all().order_by('name')
    serializer_class = EquipmentSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['lab', 'condition', 'status', 'category']
    search_fields    = ['name', 'equipment_code', 'category']


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all().order_by('-report_date')
    serializer_class = MaintenanceSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'equipment']
    search_fields    = ['reported_by', 'assigned_technician', 'issue_description']
