from django.contrib import admin
from .models import Hostel, Room, HostelStudent, RoomAllocation, HostelFee, MaintenanceRequest, VisitorEntry

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'total_rooms', 'warden_name', 'warden_mobile']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'block', 'floor', 'room_type', 'capacity', 'status']
    list_filter = ['hostel', 'status', 'floor', 'room_type']

@admin.register(HostelStudent)
class HostelStudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'department', 'year', 'mobile']
    search_fields = ['name', 'roll_number']

@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'hostel', 'check_in_date', 'is_active']
    list_filter = ['is_active', 'hostel']

@admin.register(HostelFee)
class HostelFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'amount', 'month', 'due_date', 'status']
    list_filter = ['status', 'hostel']

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'category', 'priority']

@admin.register(VisitorEntry)
class VisitorEntryAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'student', 'relation', 'in_time', 'status']
    list_filter = ['status', 'hostel']
