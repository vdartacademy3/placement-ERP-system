from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Accounts & Colleges
    path('api/auth/', include('apps.accounts.urls')),
    path('api/colleges/', include('apps.colleges.urls')),

    # Core modules
    path('api/', include('exams.urls')),
    path('api/', include('students.urls')),
    path('api/placement/', include('placement.urls')),

    # Other modules
    path('api/transport/', include('transport.urls')),
    path('api/hostel/', include('hostel.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/departments/', include('department.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
