from django.contrib import admin
from .models import Route, Stop, Driver, Bus, StudentProfile, TransportPass, Trip, TripAttendance, Maintenance, FuelLog, Notification

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'distance_km', 'estimated_time_min', 'morning_timing', 'evening_timing']

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['name', 'route', 'landmark', 'order']
    list_filter = ['route']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number', 'mobile', 'experience_years', 'is_active']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'registration_number', 'capacity', 'driver', 'route', 'status']
    list_filter = ['status', 'route']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'user', 'department', 'year', 'route', 'stop']
    list_filter = ['department', 'year', 'route']

@admin.register(TransportPass)
class TransportPassAdmin(admin.ModelAdmin):
    list_display = ['student', 'route', 'stop', 'status', 'valid_from', 'valid_until']
    list_filter = ['status']

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['bus', 'driver', 'route', 'trip_type', 'status', 'date']
    list_filter = ['status', 'trip_type', 'date']

@admin.register(TripAttendance)
class TripAttendanceAdmin(admin.ModelAdmin):
    list_display = ['trip', 'student', 'status', 'boarded_at']

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['bus', 'maintenance_type', 'scheduled_date', 'status', 'cost']
    list_filter = ['status', 'maintenance_type']

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ['bus', 'liters', 'cost_per_liter', 'total_cost', 'filled_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'recipient', 'is_broadcast', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_broadcast', 'is_read']
