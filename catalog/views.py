from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Book, CartItem, Order
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q


# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_books': num_books, }
    )


def book_list_search(request):
    print(request.GET)
    keyword = request.GET.get("keyword")
    print(keyword)
    book_list = None
    if keyword.strip() == "":
        book_list = Book.objects.all().order_by("-sales_volume")
    else:
        book_list = Book.objects.filter(
            Q(book_name__icontains=keyword) | Q(isbn=keyword) | Q(author=keyword) | Q(summary__icontains=keyword))

    print(book_list)
    return render(
        request,
        'catalog/book_list.html',
        {"book_list": book_list}
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all().order_by("-sales_volume")


class BookDetailView(generic.DetailView):
    model = Book


@login_required
def cart(request):
    uid = request.session.get('_auth_user_id')
    carts = CartItem.objects.filter(user_id=uid, order=None)
    print(carts.values())
    context = {
        'title': '购物车',
        'carts': carts,
        'book_num': carts.count(),
        'total_sum': carts.count()
    }
    return render(request, 'carts.html', context)


@login_required
def cart_add(requset, book_id, book_sum):
    print(book_id)
    print()
    book_id = int(book_id)
    book_sum = int(book_sum)
    print(dict(requset.session))
    uid = requset.session.get('_auth_user_id')
    carts = CartItem.objects.filter(book_id=book_id, user_id=uid, order=None)
    if len(carts) >= 1:
        cart = carts[0]
        cart.book_sum += book_sum
    else:
        cart = CartItem()
        cart.user_id = uid
        cart.book_id = book_id
        cart.book_sum = book_sum
    cart.save()
    if requset.is_ajax():
        book_sum = CartItem.objects.filter(user_id=uid, order=None).count()
        return JsonResponse({'book_sum': book_sum})

    else:
        return redirect('/cart')


def cart_edit(request, cid, book_sum):
    try:
        cart = CartItem.objects.get(pk=int(cid))
        cart.book_sum = int(book_sum)
        cart.save()
    except:
        return JsonResponse({'book_sum': book_sum})
    return JsonResponse({'book_sum': 0})


def cart_delete(request, cid):
    try:
        cart = CartItem.objects.get(pk=int(cid))
        cart.delete()
        data = {'ok': 1}
    except:
        data = {'ok': 0}
    return JsonResponse(data)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self):
        uid = self.request.session['_auth_user_id']
        return Order.objects.filter(buyer_id=uid).order_by('start_time')


class OrderDetailView(generic.DetailView):
    model = Order


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ('buyer_name', 'address', 'buyer_phone')

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        the_order = form.save()
        for cart in CartItem.objects.filter(user_id=self.request.user.id, order=None):
            cart.order = the_order
            book = Book.objects.get(id=cart.book_id)
            book.sales_volume = book.sales_volume + cart.book_sum
            book.save()
            cart.save()
        return super(OrderCreate, self).form_valid(form)
