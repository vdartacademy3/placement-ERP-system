from rest_framework import serializers

from .models import College


class CollegeSerializer(serializers.ModelSerializer):
    """
    Serializer for College model.
    """

    class Meta:
        model = College
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )