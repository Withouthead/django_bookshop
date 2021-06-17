from django.db import models
from django.urls import reverse


# Create your models here.
from django.utils.safestring import mark_safe


class BookType(models.Model):
    book_type = models.CharField(verbose_name="类型", max_length=20, help_text="请输入类型名称")

    def __str__(self):
        return self.book_type


class Book(models.Model):
    book_name = models.CharField(verbose_name="书名", max_length=20, help_text="Enter book name")
    isbn = models.CharField(verbose_name="ISBN号", max_length=13, help_text="请输入13位ISBN号")
    author = models.CharField(verbose_name="作者", max_length=20, help_text="请输入作者名")
    language = models.CharField(verbose_name="语言", max_length=20, help_text="请输入该书使用语言", default="中文")
    publishing_house = models.CharField(verbose_name="出版商",max_length=20, help_text="请输入出版商")
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
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.book_type.all()[:3] ])
    display_type.short_description = '类型'

    def get_image(self):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=self.book_image.url,
            width=self.book_image.width,
            height=self.book_image.height,
            )
        )