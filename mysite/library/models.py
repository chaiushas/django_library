from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
import uuid


# Create your models here.
# Django visada sukuria id
class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text="Įveskite knygos žanrą (pvz: detektyvas)")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'


class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100, help_text="Įveskite autoriaus vardą")
    last_name = models.CharField("Pavardė", max_length=100, help_text="Įveskite autoriaus pavardę")
    description = models.TextField("Aprasymas", max_length=1000, default="", help_text="Autoriaus aprasymas")
    description = HTMLField("Aprasymas")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def display_books(self):
        books = self.books.all()
        book_names = list(book.title for book in books)
        books_str = ', '.join(book_names)
        return books_str

    display_books.short_description = "Knygos"

    class Meta:
        verbose_name = 'Autorius'
        verbose_name_plural = 'Autoriai'
        ordering = ['first_name']


class Book(models.Model):
    title = models.CharField("Pavadinimas", max_length=200, help_text="Įveskite knygos pavadinimą")
    summary = models.TextField("Aprašymas", max_length=1000, help_text="Įveskite knygos aprašymą")
    isbn = models.CharField("ISBN", max_length=13,
                            help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, related_name="books")
    genre = models.ManyToManyField("Genre", help_text="Išrinkite žanrus knygai")
    cover = models.ImageField("Virselis", upload_to='covers', null=True)

    def __str__(self):
        return f"{self.author} {self.title}"

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Žanras'

    class Meta:
        verbose_name = 'Knyga'
        verbose_name_plural = 'Knygos'
        ordering = ['-id']


class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name='instances')
    due_back = models.DateField("Bus prieinama", blank=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text="Statusas")

    def __str__(self):
        return f"{self.book} ({self.uuid}) {self.status} {self.due_back}"

    class Meta:
        verbose_name = 'Egzempliorius'
        verbose_name_plural = 'Egzemplioriai'
        ordering = ['-due_back']
