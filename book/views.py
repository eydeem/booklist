from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Book
import requests


def home(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, 'book/home.html', context)


class BookListView(ListView):
    model = Book
    template_name = 'book/home.html'
    context_object_name = 'books'
    paginate_by = 10


class AddBookView(CreateView):
    model = Book
    template_name = 'book/add_update.html'
    fields = ['title', 'author', 'date_pub',
              'number_ISBN', 'pages', 'book_covers', 'language']


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'


class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'date_pub',
              'number_ISBN', 'pages', 'book_covers', 'language']
    template_name = 'book/add_update.html'


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'book/delete.html'


def BootStrapFilterView(request):
    if request.GET:
        bk = Book.objects.all()
        title_contains_query = request.GET.get('title_contains')
        author_contains_query = request.GET.get('author_contains')
        language_contains_query = request.GET.get('language_contains')
        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')

        if title_contains_query != '' and title_contains_query is not None:
            bk = bk.filter(title__icontains=title_contains_query)

        if author_contains_query != '' and author_contains_query is not None:
            bk = bk.filter(author__icontains=author_contains_query)

        if language_contains_query != '' and language_contains_query is not None:
            bk = bk.filter(language__icontains=language_contains_query)

        if date_min != '' and date_min is not None:
            bk = bk.filter(date_pub__gte=date_min)

        if date_max != '' and date_max is not None:
            bk = bk.filter(date_pub__lte=date_max)

        context = {
            "books": bk
        }

        return render(request, "book/search.html", context)

    else:
        return render(request, "book/search.html", {})


def search_api(request):
    if 'q' in request.GET:
        keyword = request.GET.get('q')
        link = "https://www.googleapis.com/books/v1/volumes?q=" + keyword
        data = requests.get(link)
        json_data = data.json()
        volume_infos = list(
            map((lambda item: mapper(item)), json_data['items']))

        context = {"books": volume_infos}
        return render(request, "book/search_api.html", context)
    else:
        return render(request, "book/search_api.html", {})


def mapper(item):
    volume_info = item['volumeInfo']
    if 'authors' in volume_info:
        volume_info['authors'] = ' '.join(volume_info['authors'])
    if 'industryIdentifiers' in volume_info:
        lambda_industry_identifier = (
            lambda industry_identifier: industry_identifier['identifier'])
        identifiers = map(lambda_industry_identifier,
                          volume_info['industryIdentifiers'])
        volume_info['isbns'] = ' '.join(identifiers)

    return volume_info


def new_book(request):
    if request.method == 'POST':
        title = request.POST['title_i']
        author = request.POST['authors_i']
        date = request.POST['publishedDate_i']

        if len(date.split('-')) == 3:
            date_pub = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        elif len(date.split('-')) == 2:
            date_pub = datetime.datetime.strptime(date, "%Y-%m").date()
        elif len(date.split('-')) == 1:
            date_pub = datetime.datetime.strptime(date, "%Y").date()

        number_ISBN = request.POST['isbns_i']
        pages = request.POST['pageCount_i']
        book_covers = request.POST['thumbnail_i']
        language = request.POST['language_i']
        bk = Book(title=title, author=author, date_pub=date_pub, number_ISBN=number_ISBN,
                  pages=pages, book_covers=book_covers, language=language)

        bk.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponse("Error")
