from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="50" height="50" />')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'get_image', 'get_qrcode', 'price', 'quantity', 'created_at')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="50" height="50" />')

    def get_qrcode(self, product):
        if product.qr_code:
            return mark_safe(f'<img src="{product.qr_code.url}" width="50" height="50" />')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ExportProduct)
admin.site.register(models.EnterProduct)
admin.site.register(models.ReturnProduct)
