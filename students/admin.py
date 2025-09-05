from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Demo, Tag

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('short_title', 'classes', 'eras', 'complexity', 'year', 'book_type')
    list_filter = ('classes', 'eras', 'book_type', 'complexity')
    search_fields = ('short_title', 'full_title', 'description')
    ordering = ('classes', 'short_title', 'complexity')

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'theme', 'difficulty')
    list_filter = ('theme', 'difficulty')
    search_fields = ('title', 'description', 'slug',)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)