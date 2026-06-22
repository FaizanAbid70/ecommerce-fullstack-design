from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price', 'stock', 'is_featured', 'in_stock')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description', 'category')
    list_editable = ('price', 'stock', 'is_featured')
    ordering = ('-created_at',)
