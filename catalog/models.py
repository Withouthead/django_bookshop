from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils.safestring import mark_safe
from decimal import Decimal

class BookType(models.Model):
    book_type = models.CharField(verbose_name="类型", max_length=20, help_text="请输入类型名称")

    def __str__(self):
        return self.book_type

    class Meta:
        verbose_name = "类型"
        verbose_name_plural = "类型"


class Book(models.Model):
    book_name = models.CharField(verbose_name="书名", max_length=20, help_text="Enter book name")
    isbn = models.CharField(verbose_name="ISBN号", max_length=13, help_text="请输入13位ISBN号")
    author = models.CharField(verbose_name="作者", max_length=20, help_text="请输入作者名")
    language = models.CharField(verbose_name="语言", max_length=20, help_text="请输入该书使用语言", default="中文")
    publishing_house = models.CharField(verbose_name="出版商", max_length=20, help_text="请输入出版商")
    publication_date = models.DateField(verbose_name="出版日期", help_text="请输入出版日期")
    summary = models.TextField(verbose_name="简介", max_length=1000, help_text="请输入介绍", null=True, blank=True)
    wholesale_price = models.DecimalField(verbose_name="进货价", max_digits=5, decimal_places=2, help_text="进货价")
    selling_price = models.DecimalField(verbose_name="销售价", max_digits=5, decimal_places=2, help_text="销售价")
    book_type = models.ManyToManyField(BookType)
    book_image = models.ImageField(verbose_name="缩略图", upload_to="book_image")
    sales_volume = models.IntegerField(verbose_name="销量", help_text="销量", default=0)

    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_type(self):
        return ', '.join([genre.name for genre in self.book_type.all()[:3]])

    display_type.short_description = '类型'

    def get_image(self):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=self.book_image.url,
            width=self.book_image.width,
            height=self.book_image.height,
        )
        )

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"

class evaluation(models.Model):
    content = models.TextField(verbose_name="评价内容", max_length=250, default="请输入评价")
    score = models.IntegerField(verbose_name="分数", default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    book = models.ForeignKey(Book, verbose_name="评价书本", on_delete=models.CASCADE)
    eval_user = models.ForeignKey(User, verbose_name="评价用户", on_delete=models.CASCADE)  # 级联

    def __str__(self):
        return self.eval_user.username + "的评论"
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"

class Order(models.Model):
    buyer_name = models.CharField(verbose_name="收货人", max_length=20)
    start_time = models.DateTimeField(verbose_name="下单时间", auto_now_add=True)
    change_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    end_time = models.DateTimeField(verbose_name="完成时间", null=True, blank=True)
    #total_cost = models.DecimalField(verbose_name="总金额", decimal_places=2, max_digits=300)
    buyer = models.ForeignKey(User, verbose_name="购买用户", on_delete=models.CASCADE)
    address = models.CharField(verbose_name="送货地址", max_length=200)
    buyer_phone = models.CharField(verbose_name="手机号", max_length=11)
    order_status_choice = (
        (0, "订单正在处理"),
        (1, "订单正在配送"),
        (2, "订单已完成"),
        (3, "订单已退回")
    )
    order_status = models.IntegerField(verbose_name="订单状态", validators=(MaxValueValidator(3), MinValueValidator(0)),
                                       choices=order_status_choice, default=0)
    def __str__(self):
        return "订单" + str(self.id)
    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])
    def get_total_cost(self):
        carts = CartItem.objects.filter(order_id=self.id)
        total_cost = Decimal(0.00)#models.DecimalField(max_digits=20000, decimal_places=2, default=0.00)
        for cart in carts:
            total_cost += cart.book_sum * cart.book.selling_price
        return total_cost
    def get_cart_items(self):
        carts = CartItem.objects.filter(order_id=self.id)
        return carts

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
class CartItem(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="购买的图书", on_delete=models.CASCADE)
    book_sum = models.IntegerField(verbose_name="购买数量", validators=(MinValueValidator(0),), default=1)
    order = models.ForeignKey(Order, verbose_name="订单", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "购买的图书:" + " " + self.book.book_name

    def get_total_sum(self):
        return self.book.selling_price * self.book_sum

    class Meta:
        verbose_name = "购买的图书"
        verbose_name_plural = "购买的图书"
