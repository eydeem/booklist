from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_pub = models.DateField()
    number_ISBN = models.CharField(max_length=100)
    pages = models.IntegerField(blank = True, default=0)
    book_covers = models.URLField(blank = True)
    language = models.CharField(max_length=100, blank = True)


    def get_absolute_url(self):
        return reverse('book-home')