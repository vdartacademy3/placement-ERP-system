from .models import College


class CollegeService:
    """
    Business logic for College operations.
    """

    @staticmethod
    def create_college(validated_data):
        return College.objects.create(**validated_data)