from django.db import models
from django.core.validators import RegexValidator


def generate_roll_number():
    """Auto-generate roll number like STU2024001"""
    from datetime import date
    year = date.today().year
    last = Student.objects.filter(roll_number__startswith=f'STU{year}').order_by('id').last()
    if last:
        last_num = int(last.roll_number[-3:])
        return f'STU{year}{str(last_num + 1).zfill(3)}'
    return f'STU{year}001'


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated')]

    # Auto-generated unique roll number
    roll_number = models.CharField(max_length=20, unique=True, blank=True)

    # Personal info
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    email        = models.EmailField(unique=True)
    phone        = models.CharField(
                       max_length=15,
                       validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
                   )
    date_of_birth = models.DateField()
    gender        = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address       = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    # Academic info
    department    = models.CharField(max_length=100)
    course        = models.CharField(max_length=100)
    year_of_study = models.PositiveSmallIntegerField()
    admission_date = models.DateField(auto_now_add=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.roll_number:
            self.roll_number = generate_roll_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.roll_number} - {self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class StudentDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id_proof',     'ID Proof'),
        ('marksheet',    'Marksheet'),
        ('certificate',  'Certificate'),
        ('photo',        'Photo'),
        ('other',        'Other'),
    ]

    student       = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title         = models.CharField(max_length=100)
    file          = models.FileField(upload_to='students/documents/')
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.roll_number} - {self.title}'
