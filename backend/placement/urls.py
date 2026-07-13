from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, StudentViewSet, PlacementDriveViewSet,
    JobOpeningViewSet, ApplicationViewSet, InterviewViewSet,
    InternshipViewSet, ResumeViewSet, PlacementRecordViewSet,
    NotificationViewSet, user_profile
)

router = DefaultRouter()
router.register(r'companies',         CompanyViewSet)
router.register(r'students',          StudentViewSet)
router.register(r'drives',            PlacementDriveViewSet,  basename='drives')
router.register(r'jobs',              JobOpeningViewSet)
router.register(r'applications',      ApplicationViewSet)
router.register(r'interviews',        InterviewViewSet)
router.register(r'internships',       InternshipViewSet)
router.register(r'resumes',           ResumeViewSet)
router.register(r'placement-records', PlacementRecordViewSet, basename='placement-records')
router.register(r'notifications',     NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/profile/', user_profile),
]
