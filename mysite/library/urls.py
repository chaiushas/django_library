from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # is mysite/library/views.py iskvieciamas index
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),  # naudojama su klasem
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book'),
    path('search/', views.search, name='search'),
    path('userbooks/', views.UserBookInstanceListView.as_view(), name='userbooks'),
    path('register/', views.register, name='register'),
]
