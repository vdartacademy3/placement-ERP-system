from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    cgpa = models.FloatField(null=True, blank=True)
    skills = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlacementDrive(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='drives')
    drive_date = models.DateField()
    eligibility_criteria = models.TextField(blank=True)
    job_role = models.CharField(max_length=100, blank=True)
    package = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobOpening(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    salary = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    student_id = models.CharField(max_length=50)
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.job.title}"


class Interview(models.Model):
    MODE_CHOICES = [('onsite', 'Onsite'), ('remote', 'Remote'), ('hybrid', 'Hybrid')]
    STATUS_CHOICES = [('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    student_id = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interviews')
    interview_date = models.DateField()
    interview_time = models.TimeField(null=True, blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='onsite')
    venue = models.CharField(max_length=200, blank=True)
    round = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.company.name} Round {self.round}"


class Internship(models.Model):
    MODE_CHOICES = [('remote', 'Remote'), ('onsite', 'Onsite'), ('hybrid', 'Hybrid')]
    STATUS_CHOICES = [('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    student_id = models.CharField(max_length=50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    stipend = models.CharField(max_length=50, blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='onsite')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student_id}"


class Resume(models.Model):
    student_id = models.CharField(max_length=50)
    file = models.FileField(upload_to='resumes/')
    file_name = models.CharField(max_length=200)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.file_name}"


class PlacementRecord(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('placed', 'Placed'),
        ('joined', 'Joined'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    PLACEMENT_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('fulltime', 'Full-Time'),
        ('ppo', 'PPO'),
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    WORK_MODE_CHOICES = [
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]
    OFFER_LETTER_CHOICES = [
        ('received', 'Received'),
        ('pending', 'Pending'),
        ('not_applicable', 'Not Applicable'),
    ]
    HIRING_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('on_hold', 'On Hold'),
    ]
    # Student Info
    student_name     = models.CharField(max_length=200)
    register_number  = models.CharField(max_length=50, unique=True)
    department       = models.CharField(max_length=100)
    year             = models.IntegerField(null=True, blank=True)
    email            = models.EmailField()
    phone            = models.CharField(max_length=20, blank=True)
    cgpa             = models.FloatField(null=True, blank=True)
    skills           = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile   = models.URLField(blank=True)
    portfolio_link   = models.URLField(blank=True)
    # Company & Job Info
    company_name        = models.CharField(max_length=200)
    company_logo        = models.ImageField(upload_to='placement/logos/', null=True, blank=True)
    job_role            = models.CharField(max_length=100, blank=True)
    job_type            = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time', blank=True)
    location            = models.CharField(max_length=200, blank=True)
    package             = models.CharField(max_length=50, blank=True)
    placement_type      = models.CharField(max_length=20, choices=PLACEMENT_TYPE_CHOICES, default='fulltime')
    work_mode           = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='onsite')
    eligibility_criteria = models.TextField(blank=True)
    required_skills     = models.TextField(blank=True)
    last_date_to_apply  = models.DateField(null=True, blank=True)
    hiring_status       = models.CharField(max_length=20, choices=HIRING_STATUS_CHOICES, default='open', blank=True)
    # Status & Dates
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    interview_date      = models.DateField(null=True, blank=True)
    offer_date          = models.DateField(null=True, blank=True)
    joining_date        = models.DateField(null=True, blank=True)
    offer_letter_status = models.CharField(max_length=20, choices=OFFER_LETTER_CHOICES, default='pending')
    # Files
    resume              = models.FileField(upload_to='placement/resumes/', null=True, blank=True)
    offer_letter        = models.FileField(upload_to='placement/offer_letters/', null=True, blank=True)
    # Extra
    remarks             = models.TextField(blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name} - {self.company_name}"


class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
