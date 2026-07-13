from django.db import models
from department.models import Department

class Faculty(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('teaching',  'Currently Teaching'),
        ('on_leave',  'On Leave'),
        ('meeting',   'In Meeting'),
    ]

    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=15, blank=True)
    designation = models.CharField(max_length=100)
    department  = models.ForeignKey(
                    Department,
                    on_delete=models.SET_NULL,
                    null=True,
                    related_name='faculty_members'
                  )
    is_hod      = models.BooleanField(default=False)
    status      = models.CharField(
                    max_length=20,
                    choices=STATUS_CHOICES,
                    default='available'
                  )
    room_no     = models.CharField(max_length=10, blank=True)
    block       = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField()
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']