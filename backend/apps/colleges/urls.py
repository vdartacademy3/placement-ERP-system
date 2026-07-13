from django.urls import path

from .views import CollegeCreateAPIView

urlpatterns = [
    path(
        "",
        CollegeCreateAPIView.as_view(),
        name="create-college",
    ),
]