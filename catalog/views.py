from django.shortcuts import render
from .models import Book
from django.views import generic

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_books': num_books, }
    )
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book
