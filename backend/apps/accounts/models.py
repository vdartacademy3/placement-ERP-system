from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel


class User(BaseModel, AbstractUser):
    """
    Custom User model for College ERP.
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        COLLEGE_ADMIN = "COLLEGE_ADMIN", "College Admin"
        HOD = "HOD", "Head of Department"
        FACULTY = "FACULTY", "Faculty"
        STUDENT = "STUDENT", "Student"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    college = models.ForeignKey(
    "colleges.College",
    on_delete=models.SET_NULL,
    related_name="users",
    blank=True,
    null=True,
)

    def __str__(self):
        return self.username