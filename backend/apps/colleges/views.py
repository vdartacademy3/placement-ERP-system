from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CollegeSerializer
from .services import CollegeService


class CollegeCreateAPIView(APIView):
    """
    Create a new college.
    """

    def post(self, request):
        serializer = CollegeSerializer(data=request.data)

        if serializer.is_valid():
            college = CollegeService.create_college(
                serializer.validated_data
            )

            return Response(
                CollegeSerializer(college).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )