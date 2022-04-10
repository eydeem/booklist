from django.urls import path
from . import views
from .views import BookListView, AddBookView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name = 'book-home'),
    path('search/', views.BootStrapFilterView, name = 'book-search'),
    path('book/add/', AddBookView.as_view(), name = 'book-add'),
    path('book/<int:pk>/', BookDetailView.as_view(), name = 'book-detail'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name = 'book-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name = 'book-delete'),
    path('search_api/', views.search_api, name = 'search-api'),
    path('search_api_insert/', views.new_book , name = 'search-api-bk'),

]
