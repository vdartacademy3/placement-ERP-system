from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hostels', views.HostelViewSet)
router.register('rooms', views.RoomViewSet)
router.register('students', views.HostelStudentViewSet)
router.register('allocations', views.RoomAllocationViewSet)
router.register('fees', views.HostelFeeViewSet)
router.register('maintenance', views.MaintenanceRequestViewSet)
router.register('visitors', views.VisitorEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.hostel_dashboard),
]
