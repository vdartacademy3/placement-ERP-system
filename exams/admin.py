from django.contrib import admin
from .models import Exam, ExamSubject, StudentMark, Result


class ExamSubjectInline(admin.TabularInline):
    model = ExamSubject
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'academic_year', 'semester', 'start_date', 'end_date', 'status')
    list_filter = ('exam_type', 'status', 'academic_year', 'semester')
    search_fields = ('name', 'academic_year')
    inlines = [ExamSubjectInline]


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject_name', 'subject_code', 'exam_date', 'total_marks', 'passing_marks')
    list_filter = ('exam',)
    search_fields = ('subject_name', 'subject_code')


@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'roll_number', 'exam_subject', 'marks_obtained', 'is_absent')
    list_filter = ('exam_subject__exam', 'is_absent')
    search_fields = ('student_name', 'roll_number')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'roll_number', 'exam', 'percentage', 'grade', 'is_pass', 'is_published')
    list_filter = ('exam', 'grade', 'is_pass', 'is_published')
    search_fields = ('student_name', 'roll_number')
    readonly_fields = ('generated_at', 'published_at')
