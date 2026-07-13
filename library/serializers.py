from rest_framework import serializers
from .models import Book, IssuedBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "isbn", "category", "publisher", "year",
            "copies", "available", "shelf", "block", "floor",
            "rack_number", "shelf_number", "position", "location_code",
        ]
        read_only_fields = ["available", "location_code"]

    def validate_copies(self, value):
        if value < 1:
            raise serializers.ValidationError("At least 1 copy required.")
        return value

    def validate_isbn(self, value):
        if not value.strip():
            raise serializers.ValidationError("ISBN is required.")
        return value


class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = [
            "id", "book", "book_title", "student_id", "student_name",
            "issue_date", "due_date", "return_date", "fine", "status",
        ]

    def validate(self, data):
        book = data.get("book")
        if book and book.available < 1:
            raise serializers.ValidationError({"book": "No copies available for this book."})
        return data
