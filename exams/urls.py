from django.urls import path, include
from rest_framework_nested import routers
from .views import ExamViewSet, ExamSubjectViewSet, StudentMarkViewSet, ResultViewSet

# Top-level router
router = routers.DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'results', ResultViewSet, basename='result')

# Nested: /exams/{exam_pk}/subjects/
exams_router = routers.NestedDefaultRouter(router, r'exams', lookup='exam')
exams_router.register(r'subjects', ExamSubjectViewSet, basename='exam-subject')

# Nested: /exams/{exam_pk}/subjects/{subject_pk}/marks/
subjects_router = routers.NestedDefaultRouter(exams_router, r'subjects', lookup='subject')
subjects_router.register(r'marks', StudentMarkViewSet, basename='subject-mark')

# Nested: /exams/{exam_pk}/results/
exams_router.register(r'results', ResultViewSet, basename='exam-result')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(exams_router.urls)),
    path('', include(subjects_router.urls)),
]
