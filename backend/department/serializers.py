from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    faculty_count = serializers.SerializerMethodField()

    class Meta:
        model  = Department
        fields = ['id', 'name', 'description',
                  'faculty_count', 'created_at']

    def get_faculty_count(self, obj):
        return obj.faculty_members.filter(is_active=True).count()