from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Route, Stop, Driver, Bus, StudentProfile, TransportPass,
    Trip, TripAttendance, Maintenance, FuelLog, Notification
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StopSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Stop
        fields = '__all__'

    def get_student_count(self, obj):
        return StudentProfile.objects.filter(stop=obj).count()


class RouteSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True, read_only=True)
    bus_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'

    def get_bus_count(self, obj):
        return obj.buses.count()

    def get_student_count(self, obj):
        return StudentProfile.objects.filter(route=obj).count()


class DriverSerializer(serializers.ModelSerializer):
    bus_number = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'

    def get_bus_number(self, obj):
        if hasattr(obj, 'bus') and obj.bus:
            return obj.bus.bus_number
        return None


class BusSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    maintenance_due = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = '__all__'

    def get_driver_name(self, obj):
        return obj.driver.name if obj.driver else None

    def get_route_name(self, obj):
        return obj.route.name if obj.route else None

    def get_student_count(self, obj):
        if obj.route:
            return StudentProfile.objects.filter(route=obj.route).count()
        return 0

    def get_maintenance_due(self, obj):
        from datetime import date, timedelta
        if obj.next_service_date:
            return obj.next_service_date <= date.today() + timedelta(days=20)
        return False


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    route_name = serializers.SerializerMethodField()
    stop_name = serializers.SerializerMethodField()
    pass_status = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def get_route_name(self, obj):
        return obj.route.name if obj.route else None

    def get_stop_name(self, obj):
        return obj.stop.name if obj.stop else None

    def get_pass_status(self, obj):
        if hasattr(obj, 'transport_pass'):
            return obj.transport_pass.status
        return None


class TransportPassSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_roll = serializers.SerializerMethodField()
    student_dept = serializers.SerializerMethodField()
    student_year = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()
    stop_name = serializers.SerializerMethodField()
    student_photo = serializers.SerializerMethodField()

    class Meta:
        model = TransportPass
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_student_roll(self, obj):
        return obj.student.roll_number

    def get_student_dept(self, obj):
        return obj.student.department

    def get_student_year(self, obj):
        return obj.student.year

    def get_route_name(self, obj):
        return obj.route.name if obj.route else None

    def get_stop_name(self, obj):
        return obj.stop.name if obj.stop else None

    def get_student_photo(self, obj):
        request = self.context.get('request')
        if obj.student.photo and request:
            return request.build_absolute_uri(obj.student.photo.url)
        return None


class TripSerializer(serializers.ModelSerializer):
    bus_number = serializers.SerializerMethodField()
    driver_name = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()
    boarded_count = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'

    def get_bus_number(self, obj):
        return obj.bus.bus_number if obj.bus else None

    def get_driver_name(self, obj):
        return obj.driver.name if obj.driver else None

    def get_route_name(self, obj):
        return obj.route.name if obj.route else None

    def get_boarded_count(self, obj):
        return obj.attendances.filter(status='boarded').count()


class TripAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_roll = serializers.SerializerMethodField()

    class Meta:
        model = TripAttendance
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_student_roll(self, obj):
        return obj.student.roll_number


class MaintenanceSerializer(serializers.ModelSerializer):
    bus_number = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = '__all__'

    def get_bus_number(self, obj):
        return obj.bus.bus_number


class FuelLogSerializer(serializers.ModelSerializer):
    bus_number = serializers.SerializerMethodField()

    class Meta:
        model = FuelLog
        fields = '__all__'

    def get_bus_number(self, obj):
        return obj.bus.bus_number


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['student', 'driver', 'manager'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        if role == 'manager':
            user.is_staff = True
            user.save()
        return user
