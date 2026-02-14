# App 3: Filtering, Sorting, Pagination & Advanced Queries

Learn advanced GraphQL query patterns used in production applications.

## What You'll Learn

### Core Topics
- **Advanced Filtering**: Filter products by multiple criteria (name, price range, category, ratings, availability)
- **Sorting & Ordering**: Sort results by any field in ascending or descending order
- **Pagination**: Implement both offset-based and cursor-based pagination patterns
- **Query Variables**: Use variables to write reusable parameterized queries
- **Aggregations**: Calculate statistics like average prices and group data by ranges
- **Query Optimization**: Use `select_related()` and `prefetch_related()` for efficient database queries

### Patterns Covered
1. **Single Filters**: Filter by one field (e.g., "is_active: true")
2. **Range Filters**: Query within ranges (e.g., "price between $50-$200")
3. **Search Filters**: Full-text search on name field
4. **Combined Filters**: Multiple filters in one query (AND logic)
5. **Offset Pagination**: Traditional page-based pagination with page number
6. **Cursor Pagination**: Relay-style cursor pagination for better UX
7. **Sort Ascending/Descending**: Order results by any field

## Project Structure

```
app3_filtering/
├── config/
│   ├── settings.py          # Django settings (includes django_filters)
│   ├── urls.py              # GraphQL endpoint
│   ├── schema.py            # GraphQL schema with filtering logic
│   └── __init__.py
├── filtering_app/
│   ├── models.py            # Category, Product, Review models
│   ├── admin.py             # Django admin setup
│   ├── apps.py
│   └── migrations/
├── postman/
│   └── GraphQL-App3-Collection.json  # 30+ test requests
├── manage.py
├── requirements.txt
├── add_sample_data.py       # Create sample products & reviews
├── README.md                # This file
├── QUICKSTART.md            # Quick start guide
└── .gitignore
```

## Data Models

### Category Model
```python
class Category(models.Model):
    name = CharField(max_length=100)
    slug = SlugField(unique=True)
    description = TextField()
```

### Product Model
```python
class Product(models.Model):
    name = CharField(max_length=255)
    slug = SlugField()
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    discount_percent = IntegerField(default=0)
    stock_quantity = IntegerField(default=0)
    sku = CharField(max_length=100, unique=True)
    is_featured = BooleanField(default=False)
    is_active = BooleanField(default=True)
    rating = DecimalField(max_digits=3, decimal_places=1)
    review_count = IntegerField(default=0)
    published_date = DateField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Review Model
```python
class Review(models.Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    user = CharField(max_length=100)
    rating = IntegerField(choices=RATING_CHOICES)  # 1-5
    title = CharField(max_length=200)
    comment = TextField()
    is_verified_purchase = BooleanField(default=False)
    helpful_count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
```

## GraphQL Schema Overview

### Query Fields (11 total)

#### 1. Category Queries
```graphql
# Get all categories
allCategories: [CategoryType]

# Get category by ID
category(id: Int!): CategoryType
```

#### 2. Basic Product Queries
```graphql
# Get all products
allProducts: [ProductType]

# Get product by ID
product(id: Int!): ProductType
```

#### 3. Advanced Product Queries

**products_filtered** - Most powerful query with all options:
```graphql
productsFiltered(
  filters: ProductFilterInput
  sort: SortInput
  page: Int
  pageSize: Int
): ProductPaginatedType
```

**products_paginated** - Cursor-based pagination:
```graphql
productsPaginated(
  name: String
  categoryId: Int
  isActive: Boolean
  first: Int
  after: String
): ProductConnected
```

#### 4. Review Queries
```graphql
allReviews: [ReviewType]
reviewsByProduct(productId: Int!): [ReviewType]
reviewsByRating(rating: Int!): [ReviewType]
```

#### 5. Aggregation Queries
```graphql
avgProductPrice: Float              # Average of all prices
productsByPriceRange: [PriceRange]  # Count grouped by price ranges
```

## Input Types

### ProductFilterInput
Fields for filtering:
```graphql
input ProductFilterInput {
  name: String              # Partial match search
  categoryId: Int          # Exact match
  isActive: Boolean        # Exact match
  isFeatured: Boolean      # Exact match
  priceMin: Float          # Range filter (>=)
  priceMax: Float          # Range filter (<=)
  ratingMin: Float         # Range filter (>=)
  hasStock: Boolean        # Custom filter for stock > 0
}
```

### SortInput
```graphql
input SortInput {
  field: String!   # price, rating, createdAt, reviewCount, name
  order: String    # asc or desc (default: desc)
}
```

## GraphQL Query Examples

### 1. Simple Filtering

**Get all active products:**
```graphql
{
  productsFiltered(filters: {isActive: true}) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Search by name:**
```graphql
{
  productsFiltered(filters: {name: "laptop"}) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Filter by category:**
```graphql
{
  productsFiltered(filters: {categoryId: 1}) {
    items {
      id
      name
      category {
        name
      }
    }
    totalCount
  }
}
```

**Show only products with stock:**
```graphql
{
  productsFiltered(filters: {hasStock: true}) {
    items {
      id
      name
      stockQuantity
    }
    totalCount
  }
}
```

### 2. Price Range Filtering

**Products under $100:**
```graphql
{
  productsFiltered(filters: {priceMax: 100.0}) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Price range $100-500:**
```graphql
{
  productsFiltered(filters: {priceMin: 100.0, priceMax: 500.0}) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Premium products over $500:**
```graphql
{
  productsFiltered(filters: {priceMin: 500.0}) {
    items {
      id
      name
      price
      rating
    }
    totalCount
  }
}
```

### 3. Rating Filtering

**High-rated products (4.0+):**
```graphql
{
  productsFiltered(filters: {ratingMin: 4.0}) {
    items {
      id
      name
      rating
      reviewCount
    }
    totalCount
  }
}
```

**Best-rated products (4.5+):**
```graphql
{
  productsFiltered(filters: {ratingMin: 4.5}) {
    items {
      id
      name
      rating
      reviewCount
    }
    totalCount
  }
}
```

### 4. Sorting Examples

**Sort by price ascending (cheapest first):**
```graphql
{
  productsFiltered(
    sort: {field: "price", order: "asc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Sort by price descending (most expensive first):**
```graphql
{
  productsFiltered(
    sort: {field: "price", order: "desc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      price
    }
    totalCount
  }
}
```

**Sort by rating (best first):**
```graphql
{
  productsFiltered(
    sort: {field: "rating", order: "desc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      rating
      reviewCount
    }
    totalCount
  }
}
```

**Sort by newest first:**
```graphql
{
  productsFiltered(
    sort: {field: "createdAt", order: "desc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      createdAt
    }
    totalCount
  }
}
```

### 5. Pagination - Offset-Based

**First page (10 items):**
```graphql
{
  productsFiltered(page: 1, pageSize: 10) {
    items {
      id
      name
      price
    }
    totalCount
    page
    pageSize
    totalPages
    hasNext
    hasPrevious
  }
}
```

**Second page:**
```graphql
{
  productsFiltered(page: 2, pageSize: 10) {
    items {
      id
      name
      price
    }
    page
    totalPages
    hasNext
  }
}
```

**Custom page size (20 items per page):**
```graphql
{
  productsFiltered(page: 1, pageSize: 20) {
    items {
      id
      name
      price
    }
    totalCount
    pageSize
  }
}
```

### 6. Pagination - Cursor-Based

**First 10 products:**
```graphql
{
  productsPaginated(first: 10) {
    edges {
      cursor
      node {
        id
        name
        price
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```

**Next page using cursor:**
```graphql
{
  productsPaginated(first: 10, after: "Y3Vyc29yOjEw") {
    edges {
      cursor
      node {
        id
        name
        price
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### 7. Combined Filters + Sort + Pagination

**Featured products under $100, sorted by rating, page 1:**
```graphql
{
  productsFiltered(
    filters: {isFeatured: true, priceMax: 100.0}
    sort: {field: "rating", order: "desc"}
    page: 1
    pageSize: 5
  ) {
    items {
      id
      name
      price
      isFeatured
      rating
    }
    totalCount
    page
    totalPages
  }
}
```

**Electronics in stock, high-rated, cheap, newest first:**
```graphql
{
  productsFiltered(
    filters: {
      categoryId: 1
      isActive: true
      hasStock: true
      ratingMin: 4.5
      priceMax: 200.0
    }
    sort: {field: "createdAt", order: "desc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      price
      rating
      stockQuantity
      category {
        name
      }
    }
    totalCount
  }
}
```

**Search + price filter + sort:**
```graphql
{
  productsFiltered(
    filters: {name: "shirt", priceMin: 20.0, priceMax: 50.0}
    sort: {field: "price", order: "asc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      price
      discountPercent
    }
    totalCount
  }
}
```

### 8. Query Variables (Reusable Queries)

**Define parameterized query:**
```graphql
query GetProductsByFilter(
  $categoryId: Int
  $minPrice: Float
  $maxPrice: Float
  $isActive: Boolean
) {
  productsFiltered(
    filters: {
      categoryId: $categoryId
      priceMin: $minPrice
      priceMax: $maxPrice
      isActive: $isActive
    }
  ) {
    items {
      id
      name
      price
      category {
        name
      }
    }
    totalCount
  }
}
```

**Pass variables:**
```json
{
  "categoryId": 1,
  "minPrice": 50,
  "maxPrice": 300,
  "isActive": true
}
```

**Reusable pagination query with variables:**
```graphql
query SearchProducts(
  $searchTerm: String
  $page: Int
  $pageSize: Int
  $sortField: String
  $sortOrder: String
) {
  productsFiltered(
    filters: {name: $searchTerm}
    sort: {field: $sortField, order: $sortOrder}
    page: $page
    pageSize: $pageSize
  ) {
    items {
      id
      name
      price
      rating
    }
    totalCount
    totalPages
  }
}
```

**Pass variables for search:**
```json
{
  "searchTerm": "keyboard",
  "page": 1,
  "pageSize": 10,
  "sortField": "rating",
  "sortOrder": "desc"
}
```

### 9. Review Queries

**All reviews:**
```graphql
{
  allReviews {
    id
    user
    rating
    title
    comment
    isVerifiedPurchase
    product {
      name
    }
  }
}
```

**Reviews for a product:**
```graphql
{
  reviewsByProduct(productId: 1) {
    id
    user
    rating
    title
    comment
    helpfulCount
  }
}
```

**5-star reviews:**
```graphql
{
  reviewsByRating(rating: 5) {
    id
    user
    product {
      name
    }
    title
    comment
  }
}
```

### 10. Aggregation Queries

**Average product price:**
```graphql
{
  avgProductPrice
}
```

Response:
```json
{
  "data": {
    "avgProductPrice": 245.75
  }
}
```

**Products grouped by price range:**
```graphql
{
  productsByPriceRange {
    priceRange
    count
  }
}
```

Response:
```json
{
  "data": {
    "productsByPriceRange": [
      {"priceRange": "0-50", "count": 5},
      {"priceRange": "50-100", "count": 8},
      {"priceRange": "100-500", "count": 12},
      {"priceRange": "500+", "count": 3}
    ]
  }
}
```

## Key Concepts

### FilterSet (django-filter)
Combines multiple filters for QuerySet filtering:
```python
class ProductFilterSet(FilterSet):
    name = CharFilter(lookup_expr='icontains')  # Case-insensitive search
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    rating_min = NumberFilter(field_name='rating', lookup_expr='gte')
    has_stock = BooleanFilter(method='filter_has_stock')
    
    class Meta:
        model = Product
        fields = ['category', 'is_active', 'is_featured']
```

### Resolver with Filtering
```python
def resolve_products_filtered(self, info, filters=None, sort=None, page=1, page_size=10):
    queryset = Product.objects.select_related('category')
    
    # Apply filters conditionally
    if filters:
        if filters.name:
            queryset = queryset.filter(name__icontains=filters.name)
        if filters.price_min:
            queryset = queryset.filter(price__gte=filters.price_min)
        # ... more filters
    
    # Apply sorting
    if sort:
        field = sort.field
        order = '-' if sort.order == 'desc' else ''
        queryset = queryset.order_by(f'{order}{field}')
    
    # Pagination
    total_count = queryset.count()
    offset = (page - 1) * page_size
    items = queryset[offset:offset + page_size]
    
    return ProductPaginatedType(
        items=items,
        total_count=total_count,
        page=page,
        page_size=page_size
    )
```

### Cursor Pagination
```python
def resolve_products_paginated(self, info, first=10, after=None, **kwargs):
    queryset = Product.objects.select_related('category')
    
    # Decode cursor and apply offset
    if after:
        after_id = decode_cursor(after)
        queryset = queryset.filter(id__gt=after_id)
    
    # Fetch one extra to determine hasNextPage
    items = list(queryset[:first + 1])
    has_next = len(items) > first
    items = items[:first]
    
    edges = [
        ProductEdge(
            cursor=encode_cursor(item.id),
            node=item
        )
        for item in items
    ]
    
    return ProductConnection(edges=edges, pageInfo=PageInfo(...))
```

### Aggregation Queries
```python
from django.db.models import Avg, Count, DecimalField, Case, When

def resolve_avg_product_price(self, info):
    return Product.objects.aggregate(
        avg_price=Avg('price')
    )['avg_price']

def resolve_products_by_price_range(self, info):
    ranges = [
        {'range': '0-50', 'min': 0, 'max': 50},
        {'range': '50-100', 'min': 50, 'max': 100},
        # ...
    ]
    
    result = []
    for r in ranges:
        count = Product.objects.filter(
            price__gte=r['min'],
            price__lt=r['max']
        ).count()
        result.append({'priceRange': r['range'], 'count': count})
    
    return result
```

## How Filtering Works

### Step 1: Request with Filters
Client sends:
```graphql
{
  productsFiltered(filters: {priceMin: 100, isFeatured: true}) {
    items { id name price }
  }
}
```

### Step 2: Resolver Processes Filters
```python
if filters.price_min:
    queryset = queryset.filter(price__gte=filters.price_min)  # >= 100
if filters.is_featured:
    queryset = queryset.filter(is_featured=True)
```

### Step 3: Database Query
```sql
SELECT * FROM filtering_app_product 
WHERE price >= 100 AND is_featured = true
```

### Step 4: Response
```json
{
  "data": {
    "productsFiltered": {
      "items": [
        {"id": "1", "name": "Laptop", "price": "1299.99"},
        {"id": "4", "name": "Monitor", "price": "599.99"}
      ]
    }
  }
}
```

## Performance Tips

### 1. Use select_related() for FK
```python
# Avoid N+1 queries
queryset = Product.objects.select_related('category')
```

### 2. Use prefetch_related() for M2M/Reverse FK
```python
queryset = Product.objects.prefetch_related('reviews')
```

### 3. Pagination Reduces Load
Always paginate instead of returning all results:
```python
items = queryset[offset:offset + page_size]  # Not queryset.all()
```

### 4. Index Common Filter Fields
```python
# In models.py
class Product(models.Model):
    is_active = BooleanField(default=True, db_index=True)
    is_featured = BooleanField(default=False, db_index=True)
    rating = DecimalField(..., db_index=True)
```

### 5. Limit Field Selection
```graphql
# Good - only request needed fields
{
  productsFiltered {
    items {
      id
      name
    }
  }
}

# Avoid - requesting everything
{
  productsFiltered {
    items {
      ... (all fields)
    }
  }
}
```

## Troubleshooting

### Issue: Filters not working
**Solution:** Ensure FilterSet field names match model field names, use `field_name` parameter if different.

### Issue: Sorting by non-existent field
**Solution:** Valid sort fields are: `price`, `rating`, `createdAt`, `reviewCount`, `name`. Check the resolver's field mapping.

### Issue: Pagination returning empty
**Solution:** Verify `page` and `pageSize` are positive integers. Page 1 is always the first page.

### Issue: Cursor pagination always empty
**Solution:** Use the exact `endCursor` returned by previous query in the `after` parameter.

### Issue: N+1 query problems
**Solution:** Use `select_related()` for ForeignKey and `prefetch_related()` for reverse relations.

## Installation & Setup

See [QUICKSTART.md](QUICKSTART.md) for step-by-step setup instructions.

## API Testing

Use the included Postman collection:
- **File:** `postman/GraphQL-App3-Collection.json`
- **Requests:** 30+ pre-built filtering, sorting, and pagination examples
- **Import:** Postman → Import → Select the JSON file

## What's Next?

After mastering App 3, explore:
- **App 4:** Authentication, Authorization & Permissions
- **App 5:** Performance & Real-time

---

**Created:** 2024  
**Updated:** 2024
