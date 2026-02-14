"""
Django Models for App 3: Filtering, Sorting, Pagination & Advanced Queries

This module demonstrates:
- Model definition for complex queries
- Field types for filtering
- Setup for pagination examples
"""

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Product category."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """E-commerce product model for filtering/pagination examples."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    
    # Inventory
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.IntegerField(default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def discounted_price(self):
        """Calculate discounted price."""
        if self.discount_percent:
            return self.price * (1 - self.discount_percent / 100)
        return self.price


class Review(models.Model):
    """Product review for filtering examples."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=100)  # Simplified: normally would be User FK
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review of {self.product.name} by {self.user}"
