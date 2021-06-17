from django.db import models
from django.urls import reverse


# Create your models here.

class BookType(models.Model):
    book_type = models.CharField(max_length=20, help_text="请输入类型名称")

    def __str__(self):
        return self.book_type


class Book(models.Model):
    book_name = models.CharField(max_length=20, help_text="Enter book name")
    isbn = models.CharField(max_length=13, help_text="请输入13位ISBN号")
    author = models.CharField(max_length=20, help_text="请输入作者名")
    language = models.CharField(max_length=20, help_text="请输入该书使用语言", default="中文")
    publishing_house = models.CharField(max_length=20, help_text="请输入出版商")
    publication_date = models.DateField(help_text="请输入出版日期")
    summary = models.TextField(max_length=1000, help_text="请输入介绍", null=True, blank=True)
    wholesale_price = models.DecimalField(max_digits=5, decimal_places=2, help_text="进货价")
    selling_price = models.DecimalField(max_digits=5, decimal_places=2, help_text="销售价")
    book_type = models.ManyToManyField(BookType)
    book_image = models.ImageField(upload_to="book_image")

    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
