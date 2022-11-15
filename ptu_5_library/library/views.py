from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Genre, Author, Book, BookInstance
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

# funckiniai viewsai visalaik reikalauja requesto (funkcijoj)

def index(request):
    # return HttpResponse("Sveiki atvyke!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instances_available_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count+1

    context = {
        'book_count': book_count,
        'book_instance_count': book_instance_count,
        "book_instances_available_count": book_instances_available_count, 
        "author_count": author_count,
        'genre_count': Genre.objects.count(),
        'visits_count': visits_count,
    }
    #objects galim kviesti ir be skliaustu

    return render(request, 'library/index.html', context=context)

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    print(type(paginator))
    page_number = request.GET.get('page')
    print(type(page_number))
    print(page_number)
    paged_authors = paginator.get_page(page_number)
    print(paged_authors)
    return render(request, "library/authors.html", {'authors': paged_authors})

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author, id=author_id)})

class BookListView(ListView):
    model = Book
    paginate_by = 2 # puslapyje bus 3 knygos
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query') # vietoj query galima bet ka poto browseri ?query=apie
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset
    #/books/?genre_id=3
    # susijusi lentele yra genre or ten yra many to many sarasas, todel kreipiames per foreign key sasaja, cia yra look - up'as, cia per joina kreipiames

    # listview klasej sitas metodaS egzistuoja
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # context['books_count'] = Book.objects.count() arba 
        context['books_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres'] = Genre.objects.all()
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id) # sita naudojam book_list.html, genre
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'   

# lazy loading su java 