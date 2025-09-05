from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    ERA_CHOICES = [
        ('soviet', 'classic', 'советская', 'классическая'),
        ('modern', 'современная'),
        ('exams', 'экзамены'),
    ]

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('djvu', 'DJVU'),
    ]

    TYPE_CHOICES = [
        ('theory', 'Теория'),
        ('exercises', 'Задачник'),
    ]

    short_title = models.CharField(max_length=100)
    full_title = models.CharField(max_length=255)
    book_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    classes = models.CharField(max_length=50)  # store as comma-separated string: "7,8,9"
    eras = models.CharField(max_length=100)    # comma-separated: "soviet,modern"
    year = models.IntegerField()
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file_link = models.FileField(upload_to='books/')
    description = models.TextField(blank=True)
    complexity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )

    def classes_list(self):
        return [c.strip() for c in self.classes.split(',')]

    def eras_list(self):
        return [e.strip() for e in self.eras.split(',')]

    def __str__(self):
        return self.short_title

class Theme(models.TextChoices):
    MATHS = 'maths', 'Математика'
    MECHANICS = 'mechanics', 'Механика'
    ELECTRODYNAMICS = 'electrodynamics', 'Электродинамика'
    THERMODYNAMICS = 'thermodynamics', 'Термодинамика'
    OPTICS = 'optics', 'оптика'
    QUANTUM = 'quantum', 'квантовая физика'

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Demo(models.Model):
    title = models.CharField(max_length=200)                          # Название
    slug = models.SlugField(unique=True)                              # URL: /demos/<slug>/
    description = models.TextField(blank=True)                        # Краткое описание
    class_levels = models.JSONField(default=list)                     # Прим.: [7, 8, 9]
    difficulty = models.PositiveSmallIntegerField(default=3)          # 1–5
    theme = models.CharField(max_length=30, choices=Theme.choices)
    tags = models.ManyToManyField(Tag, blank=True)
    icon = models.ImageField(upload_to='demos/icons/', blank=True, null=True)

    # NEW FIELDS
    theory_template = models.CharField(max_length=200, blank=True)   # e.g. 'demos/motion-plots/theory.html'
    controls_template = models.CharField(max_length=200, blank=True)
    script_static = models.CharField(max_length=200, blank=True)     # e.g. 'demos/motion-plots/script.js'

    def __str__(self):
        return self.title

    def render_theory(self):
        """Safe rendering of stored theory content."""
        return format_html(self.theory_html)
    
    def demo_file_path(instance, filename):
        return f'demos/{instance.slug}/{filename}'

class Scene(models.Model):
    demo = models.ForeignKey(Demo, related_name='scenes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField()  # optional, for internal referencing
    theory_id = models.CharField(max_length=50)  # HTML anchor id
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.demo.title} — {self.title}"
