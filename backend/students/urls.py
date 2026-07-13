from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    StudentDashboardView,
    StudentDocumentView,
    StudentDocumentDeleteView,
)

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    # Dashboard must be BEFORE router URLs to avoid conflict with students/<pk>/
    path('students/dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),

    # Document list + upload for a specific student
    path('students/<int:student_id>/documents/', StudentDocumentView.as_view(), name='student-documents'),

    # Delete a specific document
    path('students/documents/<int:doc_id>/', StudentDocumentDeleteView.as_view(), name='student-document-delete'),

    # Student CRUD + search + filter + pagination (router last)
    path('', include(router.urls)),
]
