from rest_framework import serializers
from .models import Faculty

class FacultySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model  = Faculty
        fields = [
            'id', 'name', 'email', 'phone',
            'designation', 'department', 'department_name',
            'is_hod', 'status', 'status_display',
            'room_no', 'block', 'joined_date',
            'is_active', 'created_at'
        ]