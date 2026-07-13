from django.db import models
from django.conf import settings


class Route(models.Model):
    name = models.CharField(max_length=100)
    distance_km = models.FloatField(default=0)
    estimated_time_min = models.IntegerField(default=0)
    morning_timing = models.TimeField()
    evening_timing = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.route.name} - {self.name}"


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=15)
    experience_years = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='drivers/', null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Bus(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('running', 'Running'),
        ('maintenance', 'Maintenance'),
        ('inactive', 'Inactive'),
    ]
    bus_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField(default=40)
    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='bus')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='buses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    insurance_expiry = models.DateField(null=True, blank=True)
    pollution_certificate_expiry = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    total_mileage_km = models.FloatField(default=0)
    bus_image = models.ImageField(upload_to='buses/', null=True, blank=True)
    latitude = models.FloatField(default=11.0168)
    longitude = models.FloatField(default=76.9558)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bus_number


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField(default=1)
    mobile = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    stop = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_number}"


class TransportPass(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='transport_pass')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    stop = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pass - {self.student}"


class Trip(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    TRIP_TYPE = [('morning', 'Morning'), ('evening', 'Evening')]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='trips')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE, default='morning')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    fuel_used_liters = models.FloatField(default=0)
    distance_covered_km = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.date} {self.trip_type}"


class TripAttendance(models.Model):
    STATUS_CHOICES = [('boarded', 'Boarded'), ('dropped', 'Dropped'), ('absent', 'Absent')]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    boarded_at = models.DateTimeField(null=True, blank=True)
    dropped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('trip', 'student')


class Maintenance(models.Model):
    TYPE_CHOICES = [
        ('routine', 'Routine Service'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('emergency', 'Emergency'),
    ]
    STATUS_CHOICES = [('scheduled', 'Scheduled'), ('completed', 'Completed'), ('overdue', 'Overdue')]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='routine')
    description = models.TextField(blank=True)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    mechanic_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.maintenance_type} - {self.scheduled_date}"


class FuelLog(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='fuel_logs')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    liters = models.FloatField()
    cost_per_liter = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    odometer_reading = models.FloatField(default=0)
    filled_at = models.DateTimeField(auto_now_add=True)
    filled_by = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.liters}L - {self.filled_at.date()}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('arrival', 'Bus Arriving'),
        ('delay', 'Delay'),
        ('route_change', 'Route Changed'),
        ('holiday', 'Holiday Notice'),
        ('maintenance', 'Maintenance'),
        ('general', 'General'),
    ]
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_broadcast = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
