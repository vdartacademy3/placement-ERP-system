from django.contrib import admin
from .models import Lab, Equipment, Maintenance

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display  = ['lab_code', 'name', 'department', 'lab_type', 'status']
    search_fields = ['name', 'lab_code']
    list_filter   = ['status', 'department', 'lab_type']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display  = ['equipment_code', 'name', 'lab', 'condition', 'status']
    search_fields = ['name', 'equipment_code']
    list_filter   = ['condition', 'status']

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display  = ['equipment', 'reported_by', 'status', 'report_date']
    list_filter   = ['status']
