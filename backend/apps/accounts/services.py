from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def create_user(validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user