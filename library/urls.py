from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, IssuedBookViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("issued", IssuedBookViewSet, basename="issued")

urlpatterns = [
    path("", include(router.urls)),
]
