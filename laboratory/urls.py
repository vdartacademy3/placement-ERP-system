from rest_framework.routers import DefaultRouter
from .views import LabViewSet, EquipmentViewSet, MaintenanceViewSet

router = DefaultRouter()
router.register('labs',        LabViewSet,         basename='lab')
router.register('equipment',   EquipmentViewSet,   basename='equipment')
router.register('maintenance', MaintenanceViewSet, basename='maintenance')

urlpatterns = router.urls
