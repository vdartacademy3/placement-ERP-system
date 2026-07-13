from django.db import models

LAB_TYPES = [('computer', 'Computer Lab'), ('science', 'Science Lab'), ('electronics', 'Electronics Lab'), ('research', 'Research Lab'), ('other', 'Other')]
STATUS    = [('active', 'Active'), ('inactive', 'Inactive')]

class Lab(models.Model):
    name        = models.CharField(max_length=100)
    lab_code    = models.CharField(max_length=20, unique=True, default='LAB000')
    department  = models.CharField(max_length=100, default='General')
    lab_type    = models.CharField(max_length=20, choices=LAB_TYPES, default='other')
    building    = models.CharField(max_length=100, default='Main')
    floor       = models.CharField(max_length=20, default='1')
    room_number = models.CharField(max_length=20, default='101')
    capacity    = models.PositiveIntegerField(default=0)
    incharge    = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=10, choices=STATUS, default='active')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_code} - {self.name}"


class Equipment(models.Model):
    CONDITION = [('good', 'Good'), ('repair', 'Needs Repair'), ('damaged', 'Damaged')]
    EQ_STATUS = [('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Under Maintenance')]

    lab              = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='equipment')
    name             = models.CharField(max_length=100)
    equipment_code   = models.CharField(max_length=30, unique=True, default='EQ000')
    category         = models.CharField(max_length=50, default='General')
    quantity         = models.PositiveIntegerField(default=1)
    available_qty    = models.PositiveIntegerField(default=1)
    condition        = models.CharField(max_length=10, choices=CONDITION, default='good')
    purchase_date    = models.DateField(null=True, blank=True)
    warranty_expiry  = models.DateField(null=True, blank=True)
    status           = models.CharField(max_length=15, choices=EQ_STATUS, default='available')

    def __str__(self):
        return f"{self.equipment_code} - {self.name}"


class Maintenance(models.Model):
    M_STATUS = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]

    equipment        = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance')
    issue_description= models.TextField()
    reported_by      = models.CharField(max_length=100)
    assigned_technician = models.CharField(max_length=100, blank=True)
    status           = models.CharField(max_length=15, choices=M_STATUS, default='pending')
    report_date      = models.DateField(auto_now_add=True)
    completion_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.status}"
