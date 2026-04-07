from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'brand', 'price', 'badge', 'is_active', 'order')
    list_editable = ('price', 'is_active', 'order')
    list_filter   = ('brand', 'is_active', 'accent')
    search_fields = ('name', 'brand', 'notes')
    ordering      = ('order', 'name')
