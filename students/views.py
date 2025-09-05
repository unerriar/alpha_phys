from django.shortcuts import render
import csv
from django.http import HttpResponse
from .models import Book
from .models import Demo
from django.shortcuts import get_object_or_404

def materials(request):
    theory_books = Book.objects.filter(book_type__iexact='theory')
    exercise_books = Book.objects.filter(book_type__iexact='exercises')

    return render(request, 'students/materials.html', {
        'theory_books': theory_books,
        'exercise_books': exercise_books
    })

def export_books_csv(request):
    # Prepare HTTP response as CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'short_title', 'full_title', 'book_type', 'classes',
        'eras', 'year', 'file_format', 'file_link', 'description', 'complexity'
    ])

    for book in Book.objects.all():
        writer.writerow([
            book.short_title,
            book.full_title,
            book.book_type,
            book.classes,
            book.eras,
            book.year,
            book.file_format,
            book.file_link,
            book.description,
            book.complexity
        ])

    return response

def demos(request):
    demos = Demo.objects.all().order_by('title')
    return render(request, 'students/demos.html', {'demos': demos})

def demo_detail(request, slug):
    demo = get_object_or_404(Demo, slug=slug)
    return render(request, 'students/demo.html', {'demo': demo})
