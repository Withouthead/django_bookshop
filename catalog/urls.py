from django.urls import path
from catalog import views
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('search/', views.book_list_search, name='book_search'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('carts/add/<int:book_id>/<int:book_sum>', views.cart_add, name='add_cart'),
    path('carts/edit/<int:cid>/<int:book_sum>', views.cart_edit, name='edit_cart'),
    path('carts/', views.cart, name='cart'),
    path('carts/delete/<int:cid>', views.cart_delete, name='delete_cart'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/create/', views.OrderCreate.as_view(), name='creat_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail')
    # path('book/carts/edit/<int:cid>&<int:book_sum>', views.cart_edit, name='edit_cart'),
    # path('carts/delete/<int:cid>', views.cart_delete, name='delete_cart'),
]