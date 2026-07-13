from rest_framework import serializers
from .models import Hostel, Room, HostelStudent, RoomAllocation, HostelFee, MaintenanceRequest, VisitorEntry


class RoomSerializer(serializers.ModelSerializer):
    occupied_beds = serializers.ReadOnlyField()
    available_beds = serializers.ReadOnlyField()
    hostel_name = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_hostel_name(self, obj):
        return obj.hostel.name


class HostelSerializer(serializers.ModelSerializer):
    occupied_rooms = serializers.ReadOnlyField()
    available_rooms = serializers.ReadOnlyField()
    total_students = serializers.SerializerMethodField()
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hostel
        fields = '__all__'

    def get_total_students(self, obj):
        return obj.allocations.filter(is_active=True).count()


class HostelStudentSerializer(serializers.ModelSerializer):
    current_room = serializers.SerializerMethodField()
    current_hostel = serializers.SerializerMethodField()
    fee_status = serializers.SerializerMethodField()

    class Meta:
        model = HostelStudent
        fields = '__all__'

    def get_current_room(self, obj):
        alloc = obj.allocations.filter(is_active=True).first()
        return alloc.room.room_number if alloc else None

    def get_current_hostel(self, obj):
        alloc = obj.allocations.filter(is_active=True).first()
        return alloc.hostel.name if alloc else None

    def get_fee_status(self, obj):
        fee = obj.fees.order_by('-created_at').first()
        return fee.status if fee else None


class RoomAllocationSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_roll = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()
    hostel_name = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()
    floor = serializers.SerializerMethodField()

    class Meta:
        model = RoomAllocation
        fields = '__all__'

    def get_student_name(self, obj): return obj.student.name
    def get_student_roll(self, obj): return obj.student.roll_number
    def get_room_number(self, obj): return obj.room.room_number
    def get_hostel_name(self, obj): return obj.hostel.name
    def get_block(self, obj): return obj.room.block
    def get_floor(self, obj): return obj.room.floor

    def validate(self, data):
        room = data.get('room')
        if room and room.available_beds <= 0:
            raise serializers.ValidationError('No beds available in this room.')
        student = data.get('student')
        if student and student.allocations.filter(is_active=True).exists():
            raise serializers.ValidationError('Student already has an active room allocation.')
        return data


class HostelFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_roll = serializers.SerializerMethodField()
    hostel_name = serializers.SerializerMethodField()

    class Meta:
        model = HostelFee
        fields = '__all__'

    def get_student_name(self, obj): return obj.student.name
    def get_student_roll(self, obj): return obj.student.roll_number
    def get_hostel_name(self, obj): return obj.hostel.name


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_roll = serializers.SerializerMethodField()
    hostel_name = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

    def get_student_name(self, obj): return obj.student.name
    def get_student_roll(self, obj): return obj.student.roll_number
    def get_hostel_name(self, obj): return obj.hostel.name
    def get_room_number(self, obj): return obj.room.room_number if obj.room else None


class VisitorEntrySerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_room = serializers.SerializerMethodField()
    hostel_name = serializers.SerializerMethodField()

    class Meta:
        model = VisitorEntry
        fields = '__all__'

    def get_student_name(self, obj): return obj.student.name
    def get_student_room(self, obj):
        alloc = obj.student.allocations.filter(is_active=True).first()
        return alloc.room.room_number if alloc else None
    def get_hostel_name(self, obj): return obj.hostel.name
