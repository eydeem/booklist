from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100) #moze zmienie typ na ForeignKey
    date_pub = models.DateField(blank = True)
    number_ISBN = models.IntegerField()
    pages = models.IntegerField(blank = True)
    book_covers = models.URLField(blank = True)
    language = models.CharField(max_length=100, blank = True)


    def get_absolute_url(self):
        return reverse('book-home')
        #return reverse('book-home', kwargs={'pk':self.pk}) 