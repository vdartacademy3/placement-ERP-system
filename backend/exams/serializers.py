from rest_framework import serializers
from .models import Exam, ExamSubject, StudentMark, Result


class ExamSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubject
        fields = '__all__'
        read_only_fields = ('exam',)


class StudentMarkSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='exam_subject.subject_name', read_only=True)
    subject_code = serializers.CharField(source='exam_subject.subject_code', read_only=True)
    total_marks = serializers.IntegerField(source='exam_subject.total_marks', read_only=True)
    passing_marks = serializers.IntegerField(source='exam_subject.passing_marks', read_only=True)
    is_subject_pass = serializers.SerializerMethodField()

    class Meta:
        model = StudentMark
        fields = '__all__'

    def get_is_subject_pass(self, obj):
        if obj.is_absent:
            return False
        return obj.marks_obtained >= obj.exam_subject.passing_marks


class ExamSerializer(serializers.ModelSerializer):
    exam_subjects = ExamSubjectSerializer(many=True, read_only=True)
    total_subjects = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    def get_total_subjects(self, obj):
        return obj.exam_subjects.count()


class ExamListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing exams."""
    total_subjects = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ('id', 'name', 'exam_type', 'academic_year', 'semester',
                  'start_date', 'end_date', 'status', 'total_subjects')

    def get_total_subjects(self, obj):
        return obj.exam_subjects.count()


class ResultSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    exam_type = serializers.CharField(source='exam.exam_type', read_only=True)
    academic_year = serializers.CharField(source='exam.academic_year', read_only=True)
    subject_marks = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = '__all__'

    def get_subject_marks(self, obj):
        marks = StudentMark.objects.filter(
            exam_subject__exam=obj.exam,
            student_id=obj.student_id
        ).select_related('exam_subject')
        return StudentMarkSerializer(marks, many=True).data
