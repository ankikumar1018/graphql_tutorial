"""
Django Admin configuration for App 3.
"""

from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'rating']
    search_fields = ['name', 'sku']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'description', 'category')}),
        ('Pricing', {'fields': ('price', 'discount_percent')}),
        ('Inventory', {'fields': ('stock_quantity', 'sku')}),
        ('Metadata', {'fields': ('is_featured', 'is_active', 'rating', 'review_count')}),
        ('Dates', {'fields': ('published_date', 'created_at', 'updated_at')}),
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'created_at']
    search_fields = ['product__name', 'user', 'title']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
