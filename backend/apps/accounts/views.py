from .permissions import IsSuperAdminOrCollegeAdmin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from .services import AuthService
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LogoutSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        tokens = AuthService.get_tokens_for_user(user)

        return Response(tokens, status=status.HTTP_200_OK)
    

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    permission_classes = [IsSuperAdminOrCollegeAdmin]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.create_user(serializer.validated_data)

        return Response(
            {
                "message": "User created successfully.",
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )
    

class ChangePasswordAPIView(APIView):
    """
    Change password for the currently logged-in user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set new password
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
    

class LogoutAPIView(APIView):
    """
    Logout user by blacklisting refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logged out successfully."},
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )