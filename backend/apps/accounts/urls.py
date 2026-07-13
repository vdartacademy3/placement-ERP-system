from django.urls import path

from .views import (
    LoginAPIView,
    RegisterAPIView,
    CurrentUserAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", CurrentUserAPIView.as_view(), name="current-user"),
    path("change-password/",ChangePasswordAPIView.as_view(),name="change-password",),\
    path("logout/",LogoutAPIView.as_view(),name="logout",),
]

