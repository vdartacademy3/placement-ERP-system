from django.db import models


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Mid Term'),
        ('final', 'Final'),
        ('unit_test', 'Unit Test'),
        ('practical', 'Practical'),
    ]
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('results_published', 'Results Published'),
    ]

    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    academic_year = models.CharField(max_length=9)  # e.g. "2024-2025"
    semester = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class ExamSubject(models.Model):
    """Links an exam to a subject (placeholder FK using integer ID)."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_subjects')
    subject_id = models.PositiveIntegerField()          # FK to Subject module (external)
    subject_name = models.CharField(max_length=200)     # denormalized for display
    subject_code = models.CharField(max_length=20)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)

    class Meta:
        unique_together = ('exam', 'subject_id')

    def __str__(self):
        return f"{self.exam.name} - {self.subject_name}"


class StudentMark(models.Model):
    """Stores marks obtained by a student in a subject for an exam."""
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='student_marks')
    student_id = models.PositiveIntegerField()           # FK to Student module (external)
    student_name = models.CharField(max_length=200)      # denormalized for display
    roll_number = models.CharField(max_length=50)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    is_absent = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, blank=True)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam_subject', 'student_id')

    def __str__(self):
        return f"{self.student_name} - {self.exam_subject.subject_name}: {self.marks_obtained}"


class Result(models.Model):
    """Aggregated result for a student in an exam."""
    GRADE_CHOICES = [
        ('O', 'Outstanding'),
        ('A+', 'Excellent'),
        ('A', 'Very Good'),
        ('B+', 'Good'),
        ('B', 'Above Average'),
        ('C', 'Average'),
        ('F', 'Fail'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student_id = models.PositiveIntegerField()
    student_name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=50)
    total_marks_obtained = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    is_pass = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('exam', 'student_id')
        ordering = ['-percentage']

    def __str__(self):
        return f"{self.student_name} - {self.exam.name} - {self.grade}"

    @staticmethod
    def calculate_grade(percentage):
        if percentage >= 90:
            return 'O'
        elif percentage >= 80:
            return 'A+'
        elif percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B+'
        elif percentage >= 50:
            return 'B'
        elif percentage >= 40:
            return 'C'
        return 'F'
