from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('routes', views.RouteViewSet)
router.register('stops', views.StopViewSet)
router.register('drivers', views.DriverViewSet)
router.register('buses', views.BusViewSet)
router.register('students', views.StudentProfileViewSet)
router.register('passes', views.TransportPassViewSet)
router.register('trips', views.TripViewSet)
router.register('attendance', views.TripAttendanceViewSet)
router.register('maintenance', views.MaintenanceViewSet)
router.register('fuel-logs', views.FuelLogViewSet)
router.register('notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register),
    path('auth/me/', views.me),
    path('dashboard/', views.dashboard_stats),
    path('ai/delay-prediction/', views.ai_delay_prediction),
    path('ai/seat-availability/', views.ai_seat_availability),
    path('ai/maintenance-prediction/', views.ai_maintenance_prediction),
    path('ai/route-suggestion/', views.ai_route_suggestion),
    path('ai/demand-analysis/', views.ai_demand_analysis),
    path('reports/pdf/', views.generate_pdf_report),
    path('reports/excel/', views.generate_excel_report),
]
