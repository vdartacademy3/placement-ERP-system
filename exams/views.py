from django.utils import timezone
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Exam, ExamSubject, StudentMark, Result
from .serializers import (
    ExamSerializer, ExamListSerializer,
    ExamSubjectSerializer, StudentMarkSerializer, ResultSerializer
)


class ExamViewSet(viewsets.ModelViewSet):
    """
    CRUD for Exams.
    Extra actions:
      POST /exams/{id}/generate_results/  — compute & store results for all students
      POST /exams/{id}/publish_results/   — mark results as published
    """
    queryset = Exam.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExamListSerializer
        return ExamSerializer

    @action(detail=True, methods=['post'], url_path='generate_results')
    def generate_results(self, request, pk=None):
        exam = self.get_object()
        exam_subjects = exam.exam_subjects.all()

        if not exam_subjects.exists():
            return Response(
                {'detail': 'No subjects found for this exam.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Collect all unique students who have marks in this exam
        student_ids = (
            StudentMark.objects
            .filter(exam_subject__exam=exam)
            .values_list('student_id', flat=True)
            .distinct()
        )

        if not student_ids:
            return Response(
                {'detail': 'No student marks found for this exam.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_count = 0
        updated_count = 0

        for student_id in student_ids:
            marks_qs = StudentMark.objects.filter(
                exam_subject__exam=exam,
                student_id=student_id
            ).select_related('exam_subject')

            first_mark = marks_qs.first()
            student_name = first_mark.student_name
            roll_number = first_mark.roll_number

            total_obtained = sum(
                m.marks_obtained for m in marks_qs if not m.is_absent
            )
            total_max = sum(m.exam_subject.total_marks for m in marks_qs)

            percentage = round((total_obtained / total_max * 100), 2) if total_max > 0 else 0
            grade = Result.calculate_grade(percentage)

            # Student passes only if they pass every subject
            is_pass = all(
                (not m.is_absent and m.marks_obtained >= m.exam_subject.passing_marks)
                for m in marks_qs
            )

            result, created = Result.objects.update_or_create(
                exam=exam,
                student_id=student_id,
                defaults={
                    'student_name': student_name,
                    'roll_number': roll_number,
                    'total_marks_obtained': total_obtained,
                    'total_marks': total_max,
                    'percentage': percentage,
                    'grade': grade,
                    'is_pass': is_pass,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        exam.status = 'completed'
        exam.save(update_fields=['status'])

        return Response({
            'detail': f'Results generated. Created: {created_count}, Updated: {updated_count}.',
            'total_students': len(student_ids),
        })

    @action(detail=True, methods=['post'], url_path='publish_results')
    def publish_results(self, request, pk=None):
        exam = self.get_object()
        updated = Result.objects.filter(exam=exam, is_published=False).update(
            is_published=True,
            published_at=timezone.now()
        )
        exam.status = 'results_published'
        exam.save(update_fields=['status'])
        return Response({'detail': f'{updated} result(s) published successfully.'})


class ExamSubjectViewSet(viewsets.ModelViewSet):
    """CRUD for subjects under an exam."""
    serializer_class = ExamSubjectSerializer

    def get_queryset(self):
        return ExamSubject.objects.filter(exam_id=self.kwargs['exam_pk'])

    def perform_create(self, serializer):
        exam = Exam.objects.get(pk=self.kwargs['exam_pk'])
        serializer.save(exam=exam)


class StudentMarkViewSet(viewsets.ModelViewSet):
    """
    CRUD for student marks under an exam-subject.
    Extra action:
      GET /exams/{exam_pk}/subjects/{subject_pk}/marks/by_student/?student_id=X
    """
    serializer_class = StudentMarkSerializer

    def get_queryset(self):
        return StudentMark.objects.filter(
            exam_subject_id=self.kwargs['subject_pk']
        ).select_related('exam_subject')

    @action(detail=False, methods=['get'], url_path='by_student')
    def by_student(self, request, exam_pk=None, subject_pk=None):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'detail': 'student_id query param required.'}, status=400)
        marks = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(marks, many=True)
        return Response(serializer.data)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only results.
    Extra action:
      GET /results/student/?student_id=X  — all published results for a student
    """
    serializer_class = ResultSerializer

    def get_queryset(self):
        exam_pk = self.kwargs.get('exam_pk')
        if exam_pk:
            return Result.objects.filter(exam_id=exam_pk).select_related('exam')
        return Result.objects.all().select_related('exam')

    @action(detail=False, methods=['get'], url_path='student')
    def student_results(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'detail': 'student_id query param required.'}, status=400)
        results = Result.objects.filter(
            student_id=student_id,
            is_published=True
        ).select_related('exam')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
