from django.db import models

class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('exam', 'Exam'),
        ('fee', 'Fee'),
        ('event', 'Event'),
    ]
    title    = models.CharField(max_length=255)
    message  = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_read  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
