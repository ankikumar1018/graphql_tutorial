# App 3 Quick Start Guide

Get up and running with filtering, sorting, and pagination in 5 minutes.

## Installation

### 1. Install Dependencies
```bash
cd app3_filtering
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Data
```bash
python manage.py shell < add_sample_data.py
```

Output should show:
```
✅ Sample data created successfully!
Created 4 categories
Created 17 products
Created 10 reviews
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Server runs at: **http://localhost:8000/graphql/**

## Running Your First Query

### Method 1: Using GraphQL Playground (Browser)

1. Go to http://localhost:8000/graphql/ in your browser
2. Paste this query:

```graphql
{
  allCategories {
    id
    name
  }
}
```

3. Click the play button (▶)
4. See results in the right panel

### Method 2: Using Postman

1. Open Postman
2. Import `postman/GraphQL-App3-Collection.json`
3. Select "Get All Categories" request
4. Click Send

## Essential Queries to Try

### 1. Basic Filtering

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

**Search by product name:**
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

**Products between $50-$200:**
```graphql
{
  productsFiltered(filters: {priceMin: 50.0, priceMax: 200.0}) {
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

### 3. Sorting Results

**Sort by price (cheapest first):**
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
  }
}
```

### 4. Pagination

**Get first page (10 items per page):**
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

**Go to page 2:**
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
  }
}
```

### 5. Combined Filters + Sort + Pagination

**"Show me featured products under $100, sorted by rating (best first), page 1":**
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
      rating
      reviewCount
    }
    totalCount
    totalPages
  }
}
```

### 6. Query Variables (Pro Tip)

Instead of hardcoding values, use variables:

**Query:**
```graphql
query GetProducts(
  $maxPrice: Float
  $minRating: Float
  $page: Int
  $pageSize: Int
) {
  productsFiltered(
    filters: {priceMax: $maxPrice, ratingMin: $minRating}
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
  }
}
```

**Variables (reusable):**
```json
{
  "maxPrice": 200,
  "minRating": 4.0,
  "page": 1,
  "pageSize": 10
}
```

Change variables without rewriting the query!

### 7. Aggregation Queries

**Average product price:**
```graphql
{
  avgProductPrice
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

## Available Filter Options

### ProductFilterInput Fields

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `name` | String | Search by product name (partial match) | `"laptop"` |
| `categoryId` | Int | Filter by category | `1` |
| `isActive` | Boolean | Show only active products | `true` |
| `isFeatured` | Boolean | Show only featured products | `true` |
| `priceMin` | Float | Minimum price (inclusive) | `50.0` |
| `priceMax` | Float | Maximum price (inclusive) | `200.0` |
| `ratingMin` | Float | Minimum rating | `4.5` |
| `hasStock` | Boolean | Show only products with stock | `true` |

### Valid Sort Fields

| Field | Meaning |
|-------|---------|
| `price` | Product price |
| `rating` | Product rating (1-5) |
| `createdAt` | When product was created |
| `reviewCount` | Number of reviews |
| `name` | Product name (alphabetical) |

**Sort Order:** `asc` or `desc` (default: `desc`)

## Query Response Structure

All filtering queries return:

```json
{
  "data": {
    "productsFiltered": {
      "items": [        // Array of products
        {
          "id": "1",
          "name": "Laptop Pro",
          "price": "1299.99"
        }
      ],
      "totalCount": 45,      // Total products matching filter
      "page": 1,             // Current page
      "pageSize": 10,        // Items per page
      "totalPages": 5,       // Total pages
      "hasNext": true,       // Is there a next page?
      "hasPrevious": false   // Is there a previous page?
    }
  }
}
```

## Common Use Cases

### E-commerce Search Bar
```graphql
{
  productsFiltered(
    filters: {name: "shoes", isActive: true}
    sort: {field: "rating", order: "desc"}
    page: 1
    pageSize: 20
  ) {
    items {
      id
      name
      price
      discountedPrice
      rating
      isFeatured
    }
    totalCount
  }
}
```

### Price Filter Widget
```graphql
{
  productsFiltered(
    filters: {priceMin: 50, priceMax: 500}
    page: 1
    pageSize: 50
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

### Featured Products Carousel
```graphql
{
  productsFiltered(
    filters: {isFeatured: true, isActive: true}
    sort: {field: "rating", order: "desc"}
    page: 1
    pageSize: 5
  ) {
    items {
      id
      name
      price
      discountedPrice
      rating
      image
    }
  }
}
```

### "Best Sellers" Section
```graphql
{
  productsFiltered(
    sort: {field: "reviewCount", order: "desc"}
    page: 1
    pageSize: 10
  ) {
    items {
      id
      name
      price
      reviewCount
      rating
    }
  }
}
```

### Admin Dashboard Stats
```graphql
{
  avgProductPrice
  productsByPriceRange {
    priceRange
    count
  }
}
```

## Database Info

**Database:** SQLite (auto-created in project directory)

**Tables:**
- `category` - 4 categories
- `product` - 17 products
- `review` - 10 reviews

**Reset database:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py shell < add_sample_data.py
```

## GraphQL File Locations

| File | Purpose |
|------|---------|
| `config/schema.py` | GraphQL schema definition with all resolvers |
| `filtering_app/models.py` | Product, Category, Review models |
| `postman/GraphQL-App3-Collection.json` | 30+ pre-built test requests |
| `add_sample_data.py` | Script to populate database |
| `README.md` | Detailed documentation with 50+ examples |

## Testing the API

### Method 1: GraphQL IDE (Recommended for Exploration)
```bash
http://localhost:8000/graphql/
```

### Method 2: Postman Collection
```bash
1. Import postman/GraphQL-App3-Collection.json
2. Select any request from the collection
3. Click Send
```

### Method 3: cURL (Command Line)
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{allProducts {id name price}}"
  }'
```

### Method 4: Python (Requests Library)
```python
import requests

query = """
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
"""

response = requests.post(
    'http://localhost:8000/graphql/',
    json={'query': query}
)

print(response.json())
```

## Troubleshooting

### Problem: "No module named graphene"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Database does not exist"
**Solution:** Run `python manage.py migrate`

### Problem: "No products returned"
**Solution:** Run `python manage.py shell < add_sample_data.py` to populate the database

### Problem: Filter not working
**Solution:** Check filter field names match the schema. Use exact spellings (e.g., `priceMin`, not `min_price`)

### Problem: Pagination returns empty
**Solution:** Verify `page` starts at 1 (not 0), and `pageSize` is positive

### Problem: Server not running
**Solution:** Make sure you're in the `app3_filtering` directory and run `python manage.py runserver`

## Next Steps

1. ✅ Try all the queries above
2. 📖 Read [README.md](README.md) for detailed explanations
3. 🔍 Explore the schema in `config/schema.py`
4. 💾 Examine the database relations in `filtering_app/models.py`
5. 🧪 Import the Postman collection and test 30+ real requests

## What You've Learned

- ✓ Filtering products by multiple criteria
- ✓ Sorting results in different orders
- ✓ Offset-based pagination
- ✓ Cursor-based pagination (Relay style)
- ✓ Query variables for reusable queries
- ✓ Aggregation queries (averages, grouping)
- ✓ Combining filters + sort + pagination

## Ready for More?

Check out **App 4** for:
- Authentication & Authorization
- Permission-based queries
- Token-based API security
- Role-based access control

Happy querying! 🚀
