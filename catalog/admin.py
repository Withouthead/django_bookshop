from django.contrib import admin
from .models import Book, BookType
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.

admin.site.register(BookType)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn','book_name','wholesale_price','selling_price','sales_volume')
    list_filter = ('author', 'sales_volume')
    readonly_fields = ('image_data',)  # 必须加这行 否则访问编辑页面会报错

    def image_data(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.book_image.url,
            width=obj.book_image.width,
            height=obj.book_image.height,
            )
        )

    # 页面显示的字段名称
    image_data.short_description = "书本图片"