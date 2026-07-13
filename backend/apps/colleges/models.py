from django.db import models

from apps.common.models import BaseModel


class College(BaseModel):
    """
    Represents a college registered on the ERP platform.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        max_length=15,
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    postal_code = models.CharField(
        max_length=10,
    )

    logo = models.ImageField(
        upload_to="college_logos/",
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    established_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name