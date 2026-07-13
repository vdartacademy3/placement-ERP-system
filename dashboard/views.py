from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()

@api_view(['GET'])
def dashboard_stats(request):
    stats = {
        'total_students': 0,
        'total_faculty': 0,
        'total_departments': 0,
        'total_notifications': 0,
        'total_labs': 0,
        'total_sports': 0,
        'total_cafeteria': 0,
    }

    # Import lazily to avoid circular imports
    try:
        from students.models import Student
        stats['total_students'] = Student.objects.count()
    except Exception:
        pass

    try:
        from faculty.models import Faculty
        stats['total_faculty'] = Faculty.objects.count()
    except Exception:
        pass

    try:
        from department.models import Department
        stats['total_departments'] = Department.objects.count()
    except Exception:
        pass

    try:
        from notifications.models import Notification
        stats['total_notifications'] = Notification.objects.filter(is_read=False).count()
    except Exception:
        pass

    # Laboratory, Sports, Cafeteria — static counts until those apps are built
    stats['total_labs'] = 0
    stats['total_sports'] = 0
    stats['total_cafeteria'] = 0

    return Response(stats)
