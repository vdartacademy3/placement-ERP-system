from rest_framework import serializers
from .models import Company, Student, PlacementDrive, JobOpening, Application, Interview, Internship, Resume, PlacementRecord, Notification


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class PlacementDriveSerializer(serializers.ModelSerializer):
    company_name     = serializers.CharField(source='company.name', read_only=True)
    company_location = serializers.CharField(source='company.location', read_only=True)
    applied_count    = serializers.IntegerField(read_only=True, default=0)
    selected_count   = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model  = PlacementDrive
        fields = '__all__'


class JobOpeningSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = JobOpening
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    job_title    = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'


class InternshipSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Internship
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class PlacementRecordSerializer(serializers.ModelSerializer):
    resume_url       = serializers.SerializerMethodField()
    offer_letter_url = serializers.SerializerMethodField()
    company_logo_url = serializers.SerializerMethodField()

    class Meta:
        model  = PlacementRecord
        fields = '__all__'

    def get_resume_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.resume.url) if obj.resume and req else None

    def get_offer_letter_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.offer_letter.url) if obj.offer_letter and req else None

    def get_company_logo_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.company_logo.url) if obj.company_logo and req else None


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
