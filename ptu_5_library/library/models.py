from django.db import models
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField('name', max_length=200, help_text='Enter name of book genre')

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    # papildomos f-jos duomenu bazej
    class Meta:
        ordering = ['last_name', 'first_name']

class Book(models.Model):
    title = models.CharField('title', max_length=255)
    summary = models.TextField('summary')
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True, 
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    # on_delete butina salyga
    # on_delete SET null reikia palikt null = truem, blank=true
    # protect neleis istrinti autoriaus jei jis tures knygu
    # set_null nuims autoriu, bus 'naslaites' knygos
    # cascade istrinus autoriu istrins knygas
    # do nothing (nerekomenduojama)
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)')

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"

class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name="book", on_delete=models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    ## 4 uuid yra random 3 ir 5 paduot text pagal kuri generuos, o uuid 1 pagal host id sequence nr ir current time

    LOAN_STATUS = (
        ('m', "managed"),
        ('t', "taken"),
        ('a', "available"),
        ('r', "reserved"),
    )

    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    # price = models.DecimalField('price', max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}"

    class Meta:
        ordering = ['due_back']