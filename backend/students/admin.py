from django.contrib import admin
from .models import Student, StudentDocument


class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['roll_number', 'full_name', 'email', 'department', 'course', 'year_of_study', 'status']
    search_fields = ['roll_number', 'first_name', 'last_name', 'email']
    list_filter   = ['department', 'status', 'year_of_study']
    inlines       = [StudentDocumentInline]
    readonly_fields = ['roll_number', 'admission_date', 'created_at', 'updated_at']


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'title', 'uploaded_at']
