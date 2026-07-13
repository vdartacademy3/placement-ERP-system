from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "college",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "college",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "college",
                    "phone_number",
                    "profile_image",
                )
            },
        ),
    )