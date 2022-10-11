from django.shortcuts import render, get_object_or_404, redirect
from .models import (Book, BookInstance, Author)
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin # Rodoma tik tada, kai vartotojas prisijunges

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] =  num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    context = {
        'single_author': get_object_or_404(Author, pk=author_id),
    }
    return render(request, 'author.html', context=context)


def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
    context = {
        'books': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 2  # kiek elementu bus ideta i puslapi


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'


class UserBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    context_object_name = 'instances'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by('due_back')

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')