from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Sum, Q

from .models import Hostel, Room, HostelStudent, RoomAllocation, HostelFee, MaintenanceRequest, VisitorEntry
from .serializers import (
    HostelSerializer, RoomSerializer, HostelStudentSerializer,
    RoomAllocationSerializer, HostelFeeSerializer,
    MaintenanceRequestSerializer, VisitorEntrySerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def hostel_dashboard(request):
    total_hostels = Hostel.objects.count()
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(allocations__is_active=True).distinct().count()
    available_rooms = Room.objects.filter(status='available').count()
    students_in_hostel = RoomAllocation.objects.filter(is_active=True).count()
    pending_fees = HostelFee.objects.filter(status='pending').count()
    overdue_fees = HostelFee.objects.filter(status='overdue').count()
    pending_maintenance = MaintenanceRequest.objects.filter(status='pending').count()
    in_progress_maintenance = MaintenanceRequest.objects.filter(status='in_progress').count()
    pending_visitors = VisitorEntry.objects.filter(status='pending').count()

    hostel_stats = Hostel.objects.annotate(
        student_count=Count('allocations', filter=Q(allocations__is_active=True))
    ).values('id', 'name', 'gender', 'total_rooms', 'student_count')

    fee_summary = {
        'paid': HostelFee.objects.filter(status='paid').aggregate(t=Sum('amount'))['t'] or 0,
        'pending': HostelFee.objects.filter(status='pending').aggregate(t=Sum('amount'))['t'] or 0,
        'overdue': HostelFee.objects.filter(status='overdue').aggregate(t=Sum('amount'))['t'] or 0,
    }

    maintenance_by_category = list(
        MaintenanceRequest.objects.values('category').annotate(count=Count('id')).order_by('-count')
    )

    return Response({
        'stats': {
            'total_hostels': total_hostels,
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'students_in_hostel': students_in_hostel,
            'pending_fees': pending_fees,
            'overdue_fees': overdue_fees,
            'pending_maintenance': pending_maintenance,
            'in_progress_maintenance': in_progress_maintenance,
            'pending_visitors': pending_visitors,
        },
        'hostel_stats': list(hostel_stats),
        'fee_summary': fee_summary,
        'maintenance_by_category': maintenance_by_category,
    })


class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'warden_name']


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('hostel').all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['hostel', 'status', 'floor', 'block', 'room_type']
    search_fields = ['room_number', 'block']


class HostelStudentViewSet(viewsets.ModelViewSet):
    queryset = HostelStudent.objects.all()
    serializer_class = HostelStudentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'year']
    search_fields = ['name', 'roll_number', 'department', 'mobile']


class RoomAllocationViewSet(viewsets.ModelViewSet):
    queryset = RoomAllocation.objects.select_related('student', 'room', 'hostel').all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['hostel', 'room', 'is_active']
    search_fields = ['student__name', 'student__roll_number', 'room__room_number']

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        alloc = self.get_object()
        alloc.is_active = False
        alloc.check_out_date = timezone.now().date()
        alloc.save()
        room = alloc.room
        if not room.allocations.filter(is_active=True).exists():
            room.status = 'available'
            room.save()
        return Response({'message': 'Student checked out successfully'})


class HostelFeeViewSet(viewsets.ModelViewSet):
    queryset = HostelFee.objects.select_related('student', 'hostel').all()
    serializer_class = HostelFeeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'hostel', 'student']
    search_fields = ['student__name', 'student__roll_number', 'month']
    ordering_fields = ['due_date', 'created_at']

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        fee = self.get_object()
        fee.status = 'paid'
        fee.paid_date = timezone.now().date()
        fee.transaction_id = request.data.get('transaction_id', '')
        fee.save()
        return Response({'message': 'Fee marked as paid'})


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.select_related('student', 'hostel', 'room').all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'priority', 'hostel']
    search_fields = ['student__name', 'description', 'category']
    ordering_fields = ['created_at', 'priority']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        req = self.get_object()
        req.status = request.data.get('status', req.status)
        req.assigned_to = request.data.get('assigned_to', req.assigned_to)
        if req.status == 'resolved':
            req.resolved_at = timezone.now()
        req.save()
        return Response(MaintenanceRequestSerializer(req).data)


class VisitorEntryViewSet(viewsets.ModelViewSet):
    queryset = VisitorEntry.objects.select_related('student', 'hostel').all()
    serializer_class = VisitorEntrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'hostel']
    search_fields = ['visitor_name', 'student__name', 'relation']
    ordering_fields = ['in_time', 'created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        v = self.get_object()
        v.status = 'approved'
        v.approved_by = request.data.get('approved_by', 'Warden')
        v.save()
        return Response({'message': 'Visitor approved'})

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        v = self.get_object()
        v.status = 'checked_out'
        v.out_time = timezone.now()
        v.save()
        return Response({'message': 'Visitor checked out'})
