from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date', 'isbn', 'pages')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('published_date',)
