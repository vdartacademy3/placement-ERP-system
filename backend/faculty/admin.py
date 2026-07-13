from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'email', 'department',
                     'designation', 'status', 'is_hod', 'is_active']
    search_fields = ['name', 'email']
    list_filter   = ['department', 'status', 'is_hod', 'is_active']
    ordering      = ['name'] 