from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=255, blank=True, default="")
    year = models.PositiveIntegerField(null=True, blank=True)
    copies = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    shelf = models.CharField(max_length=50, blank=True, default="")
    # Physical location
    block = models.CharField(max_length=10, blank=True, default="")
    floor = models.PositiveIntegerField(null=True, blank=True)
    rack_number = models.CharField(max_length=20, blank=True, default="")
    shelf_number = models.CharField(max_length=20, blank=True, default="")
    position = models.CharField(max_length=20, blank=True, default="")
    location_code = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.block and self.floor and self.rack_number and self.shelf_number:
            self.location_code = f"{self.block}-{self.floor}-{self.rack_number}-{self.shelf_number}"
        super().save(*args, **kwargs)


class IssuedBook(models.Model):
    STATUS_CHOICES = [
        ("Issued", "Issued"),
        ("Returned", "Returned"),
        ("Overdue", "Overdue"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
    book_title = models.CharField(max_length=255, blank=True)
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=255)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Issued")

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.student_name} — {self.book_title}"

    def save(self, *args, **kwargs):
        if not self.book_title and self.book_id:
            self.book_title = self.book.title
        super().save(*args, **kwargs)
