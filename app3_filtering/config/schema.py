"""
GraphQL Schema definition for App 3: Filtering, Sorting, Pagination & Advanced Queries

This module demonstrates:
- Filtering with django-filter
- Sorting and ordering
- Offset-based pagination
- Cursor-based pagination
- Query variables
- Aliases
- Fragments
"""

import graphene
from graphene_django import DjangoObjectType
from graphene import InputObjectType, String, Int, Float, Boolean, List
from django_filters import FilterSet, CharFilter, NumberFilter, BooleanFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from filtering_app.models import Category, Product, Review
from decimal import Decimal


# =====================================================================
# FilterSet Classes for Advanced Filtering
# =====================================================================

class ProductFilterSet(FilterSet):
    """FilterSet for Product model - supports advanced filtering."""
    
    # Exact filters
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Product name contains')
    
    # Numeric range filters
    price_min = NumberFilter(field_name='price', lookup_expr='gte', label='Min price')
    price_max = NumberFilter(field_name='price', lookup_expr='lte', label='Max price')
    rating_min = NumberFilter(field_name='rating', lookup_expr='gte', label='Min rating')
    
    # Boolean filters
    is_active = BooleanFilter(field_name='is_active', label='Is active')
    is_featured = BooleanFilter(field_name='is_featured', label='Is featured')
    has_stock = BooleanFilter(
        field_name='stock_quantity',
        method='filter_has_stock',
        label='Has stock'
    )
    
    # Ordering
    order_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'),
            ('rating', 'rating'),
            ('created_at', 'created_at'),
            ('-price', 'price_desc'),
            ('-rating', 'rating_desc'),
            ('-created_at', 'newest'),
        )
    )
    
    class Meta:
        model = Product
        fields = ['category', 'is_active', 'is_featured']
    
    def filter_has_stock(self, queryset, name, value):
        """Custom filter for products with stock."""
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)


# =====================================================================
# GraphQL ObjectTypes
# =====================================================================

class CategoryType(DjangoObjectType):
    """GraphQL type for Category."""
    products_count = graphene.Int()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'products', 'created_at']
    
    def resolve_products_count(self, info):
        """Get count of products in category."""
        return self.products.count()


class ReviewType(DjangoObjectType):
    """GraphQL type for Review."""
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'title', 'comment', 'is_verified_purchase', 'helpful_count', 'created_at']


class ProductType(DjangoObjectType):
    """GraphQL type for Product with custom fields."""
    discounted_price = graphene.Float()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'price', 'discount_percent', 
                 'stock_quantity', 'sku', 'is_featured', 'is_active', 'rating', 'review_count',
                 'created_at', 'updated_at', 'published_date', 'reviews']
    
    def resolve_discounted_price(self, info):
        """Calculate discounted price."""
        return float(self.discounted_price)


# =====================================================================
# Pagination Types (Relay-style for cursor pagination)
# =====================================================================

class ProductEdge(graphene.ObjectType):
    """Edge for cursor-based pagination."""
    node = graphene.Field(ProductType)
    cursor = graphene.String()


class ProductConnection(graphene.ObjectType):
    """Connection for cursor-based pagination."""
    edges = graphene.List(ProductEdge)
    page_info = graphene.Field(lambda: PageInfo)
    total_count = graphene.Int()


class PageInfo(graphene.ObjectType):
    """Page information for cursor pagination."""
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    start_cursor = graphene.String()
    end_cursor = graphene.String()


# =====================================================================
# Offset Pagination Type
# =====================================================================

class ProductPaginatedType(graphene.ObjectType):
    """Offset-based pagination."""
    items = graphene.List(ProductType)
    total_count = graphene.Int()
    page = graphene.Int()
    page_size = graphene.Int()
    total_pages = graphene.Int()
    has_next = graphene.Boolean()
    has_previous = graphene.Boolean()


# =====================================================================
# Filter Input Types (for query variables)
# =====================================================================

class ProductFilterInput(InputObjectType):
    """Input type for filtering products."""
    name = String(description="Product name contains")
    category_id = Int(description="Filter by category ID")
    is_active = Boolean(description="Is product active")
    is_featured = Boolean(description="Is product featured")
    price_min = Float(description="Minimum price")
    price_max = Float(description="Maximum price")
    rating_min = Float(description="Minimum rating")
    has_stock = Boolean(description="Only products with stock")


class SortInput(InputObjectType):
    """Input type for sorting results."""
    field = String(required=True, description="Field to sort by (name, price, rating, created_at)")
    order = String(description="asc or desc (default: asc)")


# =====================================================================
# Root Query with Filtering & Pagination
# =====================================================================

class Query(graphene.ObjectType):
    """Root Query type with filtering, sorting, and pagination."""
    
    # Basic queries
    all_categories = graphene.List(CategoryType, description="Get all categories")
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))
    
    # Product queries - Basic
    all_products = graphene.List(ProductType, description="Get all products")
    product = graphene.Field(ProductType, id=graphene.Int(required=True))
    
    # Product queries - With Filtering & Sorting (offset pagination)
    products_filtered = graphene.Field(
        ProductPaginatedType,
        filters=ProductFilterInput(),
        sort=SortInput(),
        page=graphene.Int(default_value=1, description="Page number (1-based)"),
        page_size=graphene.Int(default_value=10, description="Items per page"),
        description="Get filtered, sorted, and paginated products"
    )
    
    # Product queries - Cursor pagination
    products_paginated = graphene.Field(
        ProductConnection,
        name=String(description="Filter by product name"),
        category_id=Int(description="Filter by category ID"),
        is_active=Boolean(description="Is product active"),
        first=Int(description="Number of items to fetch"),
        after=String(description="Cursor for pagination"),
        description="Get products with cursor-based pagination"
    )
    
    # Review queries
    all_reviews = graphene.List(
        ReviewType,
        description="Get all reviews"
    )
    reviews_by_product = graphene.List(
        ReviewType,
        product_id=graphene.Int(required=True),
        rating=Int(description="Filter by rating"),
        description="Get reviews for a product"
    )
    reviews_by_rating = graphene.List(
        ReviewType,
        rating=graphene.Int(required=True),
        description="Get all reviews with specific rating"
    )
    
    # Stats/Aggregations
    avg_product_price = graphene.Float(description="Average product price")
    products_by_price_range = graphene.Field(
        graphene.ObjectType,
        description="Products grouped by price range"
    )
    
    # Resolvers
    def resolve_all_categories(self, info):
        return Category.objects.prefetch_related('products').all()
    
    def resolve_category(self, info, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return None
    
    def resolve_all_products(self, info):
        return Product.objects.select_related('category').prefetch_related('reviews').all()
    
    def resolve_product(self, info, id):
        try:
            return Product.objects.select_related('category').prefetch_related('reviews').get(pk=id)
        except Product.DoesNotExist:
            return None
    
    def resolve_products_filtered(self, info, filters=None, sort=None, page=1, page_size=10):
        """Advanced filtering and pagination resolver."""
        queryset = Product.objects.select_related('category').prefetch_related('reviews').all()
        
        # Apply filters
        if filters:
            if filters.name:
                queryset = queryset.filter(name__icontains=filters.name)
            if filters.category_id:
                queryset = queryset.filter(category_id=filters.category_id)
            if filters.is_active is not None:
                queryset = queryset.filter(is_active=filters.is_active)
            if filters.is_featured is not None:
                queryset = queryset.filter(is_featured=filters.is_featured)
            if filters.price_min is not None:
                queryset = queryset.filter(price__gte=filters.price_min)
            if filters.price_max is not None:
                queryset = queryset.filter(price__lte=filters.price_max)
            if filters.rating_min is not None:
                queryset = queryset.filter(rating__gte=filters.rating_min)
            if filters.has_stock is not None:
                if filters.has_stock:
                    queryset = queryset.filter(stock_quantity__gt=0)
                else:
                    queryset = queryset.filter(stock_quantity=0)
        
        # Apply sorting
        if sort:
            field_map = {
                'name': 'name',
                'price': 'price',
                'rating': 'rating',
                'created_at': 'created_at',
            }
            field = field_map.get(sort.field, 'created_at')
            order = '-' if sort.order == 'desc' else ''
            queryset = queryset.order_by(f'{order}{field}')
        else:
            queryset = queryset.order_by('-created_at')
        
        # Calculate pagination
        total_count = queryset.count()
        total_pages = (total_count + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        items = queryset[offset:offset + page_size]
        
        return ProductPaginatedType(
            items=items,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
    
    def resolve_products_paginated(self, info, name=None, category_id=None, is_active=None, first=10, after=None):
        """Cursor-based pagination resolver."""
        queryset = Product.objects.select_related('category').prefetch_related('reviews').all()
        
        # Apply filters
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        queryset = queryset.order_by('-created_at')
        
        # Simple cursor implementation (in production, use graphene-django relay)
        total_count = queryset.count()
        items = queryset[:first]
        
        edges = [
            ProductEdge(
                node=item,
                cursor=f"cursor_{item.id}"
            )
            for item in items
        ]
        
        page_info = PageInfo(
            has_next_page=total_count > first,
            has_previous_page=False,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        )
        
        return ProductConnection(
            edges=edges,
            page_info=page_info,
            total_count=total_count
        )
    
    def resolve_all_reviews(self, info):
        return Review.objects.select_related('product').all()
    
    def resolve_reviews_by_product(self, info, product_id, rating=None):
        """Get reviews for a specific product."""
        queryset = Review.objects.filter(product_id=product_id).select_related('product')
        if rating:
            queryset = queryset.filter(rating=rating)
        return queryset
    
    def resolve_reviews_by_rating(self, info, rating):
        """Get all reviews with specific rating."""
        return Review.objects.filter(rating=rating).select_related('product')
    
    def resolve_avg_product_price(self, info):
        """Calculate average product price."""
        from django.db.models import Avg
        avg = Product.objects.aggregate(Avg('price'))['price__avg']
        return float(avg) if avg else 0
    
    def resolve_products_by_price_range(self, info):
        """Group products by price range."""
        from django.db.models import Count, Case, When
        
        ranges = {
            'budget': Product.objects.filter(price__lt=50).count(),
            'mid': Product.objects.filter(price__gte=50, price__lt=200).count(),
            'premium': Product.objects.filter(price__gte=200).count(),
        }
        
        return graphene.ObjectType.create_type(
            'PriceRanges',
            {k: graphene.Int() for k in ranges}
        )(**ranges)


schema = graphene.Schema(query=Query)
