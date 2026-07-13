from django.db import models
from django.conf import settings


class Hostel(models.Model):
    GENDER_CHOICES = [('boys', 'Boys'), ('girls', 'Girls'), ('mixed', 'Mixed')]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='boys')
    total_rooms = models.IntegerField(default=0)
    floors = models.IntegerField(default=1)
    warden_name = models.CharField(max_length=100, blank=True)
    warden_mobile = models.CharField(max_length=15, blank=True)
    warden_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='hostels/', null=True, blank=True)
    amenities = models.TextField(blank=True, help_text='Comma separated')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def occupied_rooms(self):
        return self.rooms.filter(allocations__is_active=True).distinct().count()

    @property
    def available_rooms(self):
        return self.rooms.filter(status='available').count()


class Room(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('occupied', 'Occupied'), ('maintenance', 'Maintenance')]
    TYPE_CHOICES = [('single', 'Single'), ('double', 'Double'), ('triple', 'Triple'), ('dormitory', 'Dormitory')]
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    block = models.CharField(max_length=20, blank=True)
    floor = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='double')
    capacity = models.IntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=3000)
    amenities = models.TextField(blank=True)

    class Meta:
        unique_together = ('hostel', 'room_number')

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

    @property
    def occupied_beds(self):
        return self.allocations.filter(is_active=True).count()

    @property
    def available_beds(self):
        return max(0, self.capacity - self.occupied_beds)


class HostelStudent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hostel_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField(default=1)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='hostel_students/', null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_mobile = models.CharField(max_length=15, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class RoomAllocation(models.Model):
    student = models.ForeignKey(HostelStudent, on_delete=models.CASCADE, related_name='allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='allocations')
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    allocated_by = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'room', 'is_active')

    def __str__(self):
        return f"{self.student.name} - {self.room}"


class HostelFee(models.Model):
    STATUS_CHOICES = [('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')]
    student = models.ForeignKey(HostelStudent, on_delete=models.CASCADE, related_name='fees')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.month} - {self.status}"


class MaintenanceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('fan', 'Fan Not Working'), ('water', 'Water Issue'),
        ('electricity', 'Electricity'), ('wifi', 'Wi-Fi Issue'),
        ('furniture', 'Furniture'), ('cleaning', 'Cleaning'), ('other', 'Other'),
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    student = models.ForeignKey(HostelStudent, on_delete=models.CASCADE, related_name='maintenance_requests')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.CharField(max_length=100, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.category} - {self.status}"


class VisitorEntry(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('checked_out', 'Checked Out')]
    student = models.ForeignKey(HostelStudent, on_delete=models.CASCADE, related_name='visitors')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    visitor_mobile = models.CharField(max_length=15, blank=True)
    relation = models.CharField(max_length=50)
    purpose = models.TextField(blank=True)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.CharField(max_length=100, blank=True)
    id_proof = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.name}"
