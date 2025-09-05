import csv
from django.core.management.base import BaseCommand
from students.models import Book

class Command(BaseCommand):
    help = 'Import books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                book, created = Book.objects.update_or_create(
                    short_title=row['short_title'],
                    defaults={
                        'full_title': row['full_title'],
                        'book_type': row['book_type'],
                        'classes': row['classes'],
                        'eras': row['eras'],
                        'year': int(row['year']) if row['year'] else None,
                        'file_format': row['file_format'],
                        'file_link': row['file_link'],
                        'description': row['description'],
                        'complexity': int(row['complexity']) if row.get('complexity') else 3,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {book.short_title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated: {book.short_title}"))
