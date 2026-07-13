from django.contrib import admin
from .models import Book, IssuedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "category", "copies", "available", "location_code"]
    list_filter = ["category", "block"]
    search_fields = ["title", "author", "isbn"]


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ["book_title", "student_name", "student_id", "issue_date", "due_date", "status", "fine"]
    list_filter = ["status"]
    search_fields = ["student_name", "student_id", "book_title"]
