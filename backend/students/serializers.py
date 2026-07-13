from rest_framework import serializers
from .models import Student, StudentDocument


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StudentDocument
        fields = ['id', 'document_type', 'title', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class StudentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for student list page (no documents, no address)"""
    full_name = serializers.ReadOnlyField()

    class Meta:
        model  = Student
        fields = [
            'id', 'roll_number', 'full_name', 'email',
            'department', 'course', 'year_of_study', 'status', 'profile_photo'
        ]


class StudentSerializer(serializers.ModelSerializer):
    """Full serializer for create, update, profile, dashboard"""
    full_name = serializers.ReadOnlyField()
    documents = StudentDocumentSerializer(many=True, read_only=True)

    class Meta:
        model  = Student
        fields = [
            'id', 'roll_number', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'date_of_birth', 'gender', 'address',
            'profile_photo', 'department', 'course', 'year_of_study',
            'admission_date', 'status', 'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['roll_number', 'admission_date', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Ensure email is unique on create and update"""
        student_id = self.instance.id if self.instance else None
        if Student.objects.filter(email=value).exclude(id=student_id).exists():
            raise serializers.ValidationError('A student with this email already exists.')
        return value

    def validate_year_of_study(self, value):
        if value < 1 or value > 6:
            raise serializers.ValidationError('Year of study must be between 1 and 6.')
        return value


class StudentDashboardSerializer(serializers.Serializer):
    """Read-only serializer for dashboard stats"""
    total_students    = serializers.IntegerField()
    active_students   = serializers.IntegerField()
    inactive_students = serializers.IntegerField()
    graduated_students = serializers.IntegerField()
    departments       = serializers.ListField()
