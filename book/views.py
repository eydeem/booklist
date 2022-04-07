from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Book
from googleapiclient.discovery import build
import json


def home(request):
    context = {
        "books" : Book.objects.all()
    }
    return render(request, 'book/home.html', context)


class BookListView(ListView):
    model = Book
    template_name = 'book/home.html'
    context_object_name = 'books'


class AddBookView(CreateView):
    model = Book
    template_name = 'book/add_update.html'
    fields = ['title', 'author', 'date_pub', 'number_ISBN', 'pages', 'book_covers', 'language']

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'date_pub', 'number_ISBN', 'pages', 'book_covers', 'language']
    template_name = 'book/add_update.html'

class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'book/delete.html'

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Book.objects.filter(title__icontains = q)
    else:
        data = Book.objects.all()

    context = {
        'books': data
    }
    return render(request, 'book/search.html', context)


def BootStrapFilterView(request):
    bk = Book.objects.all()
    title_contains_query = request.GET.get('title_contains')
    author_contains_query = request.GET.get('author_contains')
    language_contains_query = request.GET.get('language_contains')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if title_contains_query != '' and title_contains_query is not None:
        bk = bk.filter(title__icontains = title_contains_query) 

    if author_contains_query != '' and author_contains_query is not None:
        bk = bk.filter(author__icontains = author_contains_query)

    if language_contains_query != '' and language_contains_query is not None:
        bk = bk.filter(language__icontains = language_contains_query)

    if date_min != '' and date_min is not None:
        bk = bk.filter(date_pub__gte = date_min)

    if date_max != '' and date_max is not None:
        bk = bk.filter(date_pub__gte = date_max)

    context = {
        "books": bk
    }

    return render(request, "book/search.html", context)


from django.shortcuts import render
from django.http import JsonResponse
import requests, json
from django.core import serializers


def search_api(request):
    if 'q' in request.GET:
        keyword = request.GET.get('q')
        link = "https://www.googleapis.com/books/v1/volumes?q=" + keyword
        data = requests.get(link).json()
        print("foo")

    else:
        data = Book.objects.all()
        print("foo2")



    data = serializers.serialize("json", data)
    title = []

    context = {"books" : data}


    #context = JsonResponse({'data':data})
    print(data)
    #return JsonResponse({'data':data})
    return render(request, "book/search_api.html", context)



'''
def get_books_data(query):

    service = build('books', 
                    'v1', 
                    developerKey='AIzaSyA5hmZMj80SFzvaq0COagy-QpWJ4oB3hQc',
                    )

    request = service.volumes().list(q=query)
    response = request.execute()
    book_list = [response['items'][item]['volumeInfo'] for item in range(len(response['items']))]

    return book_list


def search_api(request):
    query = request.GET.get('q')
    books = get_books_data(query)
        
    context = {
        'books': books
    }

    return render(request, 'book/search_api.html', context)
'''