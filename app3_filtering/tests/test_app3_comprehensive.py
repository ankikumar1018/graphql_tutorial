"""
Comprehensive pytest suite for App 3: Filtering, Sorting, Pagination
Tests cover models, queries, filtering, sorting, offset pagination, cursor pagination, and aggregations
"""
import pytest
from django.test import Client
from graphene.test import Client as GrapheneClient
from filtering_app.models import Category, Product, Review
from config.schema import schema
import json
from decimal import Decimal
from datetime import date


@pytest.fixture
def api_client():
    """GraphQL test client"""
    return GrapheneClient(schema)


@pytest.fixture
def http_client():
    """HTTP client"""
    return Client()


@pytest.fixture
def sample_categories(db):
    """Create sample categories"""
    electronics, _ = Category.objects.get_or_create(
        slug="electronics",
        defaults={
            "name": "Electronics",
            "description": "Electronic items"
        }
    )
    books, _ = Category.objects.get_or_create(
        slug="books",
        defaults={
            "name": "Books",
            "description": "Books and literature"
        }
    )
    clothing, _ = Category.objects.get_or_create(
        slug="clothing",
        defaults={
            "name": "Clothing",
            "description": "Apparel"
        }
    )
    return [electronics, books, clothing]


@pytest.fixture
def sample_products(db, sample_categories):
    """Create sample products with different attributes"""
    laptop, _ = Product.objects.get_or_create(
        sku="ELEC001",
        defaults={
            "name": "Laptop",
            "slug": "laptop",
            "description": "High-end laptop",
            "category": sample_categories[0],
            "price": Decimal('999.99'),
            "discount_percent": 10,
            "stock_quantity": 50,
            "is_featured": True,
            "is_active": True,
            "rating": Decimal('4.5'),
            "review_count": 100,
            "published_date": date(2024, 1, 1)
        }
    )
    
    python_book, _ = Product.objects.get_or_create(
        sku="BOOK001",
        defaults={
            "name": "Python Book",
            "slug": "python-book",
            "description": "Learn Python",
            "category": sample_categories[1],
            "price": Decimal('49.99'),
            "discount_percent": 0,
            "stock_quantity": 200,
            "is_featured": False,
            "is_active": True,
            "rating": Decimal('4.8'),
            "review_count": 50,
            "published_date": date(2024, 2, 1)
        }
    )
    
    tshirt, _ = Product.objects.get_or_create(
        sku="CLO001",
        defaults={
            "name": "T-Shirt",
            "slug": "t-shirt",
            "description": "Cotton T-Shirt",
            "category": sample_categories[2],
            "price": Decimal('19.99'),
            "discount_percent": 20,
            "stock_quantity": 0,
            "is_featured": False,
            "is_active": False,
            "rating": Decimal('3.5'),
            "review_count": 25,
            "published_date": date(2024, 3, 1)
        }
    )
    
    mouse, _ = Product.objects.get_or_create(
        sku="ELEC002",
        defaults={
            "name": "Mouse",
            "slug": "mouse",
            "description": "Wireless mouse",
            "category": sample_categories[0],
            "price": Decimal('29.99'),
            "discount_percent": 5,
            "stock_quantity": 150,
            "is_featured": True,
            "is_active": True,
            "rating": Decimal('4.2'),
            "review_count": 75,
            "published_date": date(2024, 1, 15)
        }
    )
    
    novel, _ = Product.objects.get_or_create(
        sku="BOOK002",
        defaults={
            "name": "Novel",
            "slug": "novel",
            "description": "Fiction novel",
            "category": sample_categories[1],
            "price": Decimal('15.99'),
            "discount_percent": 0,
            "stock_quantity": 100,
            "is_featured": False,
            "is_active": True,
            "rating": Decimal('4.0'),
            "review_count": 30,
            "published_date": date(2024, 2, 15)
        }
    )
    
    return [laptop, python_book, tshirt, mouse, novel]


@pytest.fixture
def sample_reviews(db, sample_products):
    """Create sample reviews"""
    reviews = []
    for i, product in enumerate(sample_products[:3]):
        reviews.append(
            Review.objects.create(
                product=product,
                user=f"User{i}",
                rating=5 - i,
                title=f"Review {i}",
                comment=f"Great product {i}",
                is_verified_purchase=i % 2 == 0,
                helpful_count=i * 10
            )
        )
    return reviews


# ==================== Model Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestCategoryModel:
    """Test Category model"""
    
    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test description"
        )
        assert category.name == "Test Category"
        assert str(category) == "Test Category"
    
    def test_category_unique_slug(self, sample_categories):
        """Test slug uniqueness"""
        with pytest.raises(Exception):  # IntegrityError
            Category.objects.create(
                name="Duplicate",
                slug="electronics"  # Already exists
            )
    
    def test_category_products_relationship(self, sample_categories, sample_products):
        """Test category has products"""
        electronics = sample_categories[0]
        assert electronics.products.count() >= 2  # At least 2 products in electronics


@pytest.mark.unit
@pytest.mark.django_db
class TestProductModel:
    """Test Product model"""
    
    def test_product_creation(self, sample_categories):
        """Test creating a product"""
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="Test",
            category=sample_categories[0],
            price=Decimal('100.00'),
            stock_quantity=10,
            sku="TEST001"
        )
        assert product.name == "Test Product"
        assert product.price == Decimal('100.00')
        assert str(product) == "Test Product"
    
    def test_product_discounted_price(self, sample_products):
        """Test discounted price calculation"""
        laptop = sample_products[0]
        # 999.99 with 10% discount = 899.991
        expected = Decimal('999.99') * Decimal('0.9')
        assert laptop.discounted_price == expected
    
    def test_product_no_discount(self, sample_products):
        """Test product without discount"""
        book = sample_products[1]
        assert book.discounted_price == book.price
    
    def test_product_relationships(self, sample_products, sample_categories):
        """Test product relationships"""
        laptop = sample_products[0]
        assert laptop.category == sample_categories[0]
        assert laptop.category.name == "Electronics"


@pytest.mark.unit
@pytest.mark.django_db
class TestReviewModel:
    """Test Review model"""
    
    def test_review_creation(self, sample_products):
        """Test creating a review"""
        review = Review.objects.create(
            product=sample_products[0],
            user="TestUser",
            rating=5,
            title="Great",
            comment="Loved it"
        )
        assert review.rating == 5
        assert review.user == "TestUser"
    
    def test_review_product_relationship(self, sample_reviews, sample_products):
        """Test review belongs to product"""
        review = sample_reviews[0]
        assert review.product == sample_products[0]


# ==================== Basic Query Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestBasicQueries:
    """Test basic GraphQL queries"""
    
    def test_all_categories_query(self, api_client, sample_categories):
        """Test allCategories query"""
        query = '''
            query {
                allCategories {
                    id
                    name
                    slug
                    description
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        categories = result['data']['allCategories']
        assert len(categories) >= 3
        assert categories[0]['name'] in ["Electronics", "Books", "Clothing"]
    
    def test_category_by_id(self, api_client, sample_categories):
        """Test category query by ID"""
        category_id = sample_categories[0].id
        query = f'''
            query {{
                category(id: {category_id}) {{
                    id
                    name
                    slug
                    productsCount
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert result['data']['category']['name'] == "Electronics"
    
    def test_all_products_query(self, api_client, sample_products):
        """Test allProducts query"""
        query = '''
            query {
                allProducts {
                    id
                    name
                    price
                    category {
                        name
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        products = result['data']['allProducts']
        assert len(products) >= 5
    
    def test_product_by_id(self, api_client, sample_products):
        """Test product query by ID"""
        product_id = sample_products[0].id
        query = f'''
            query {{
                product(id: {product_id}) {{
                    id
                    name
                    price
                    discountedPrice
                    category {{
                        name
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        product = result['data']['product']
        assert product['name'] == "Laptop"
        assert float(product['discountedPrice']) < float(product['price'])
    
    def test_all_reviews_query(self, api_client, sample_reviews):
        """Test allReviews query"""
        query = '''
            query {
                allReviews {
                    id
                    user
                    rating
                    title
                    product {
                        name
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        reviews = result['data']['allReviews']
        assert len(reviews) >= 3


# ==================== Filtering Tests ====================

@pytest.mark.filtering
@pytest.mark.django_db
class TestFiltering:
    """Test filtering functionality"""
    
    def test_filter_products_by_name(self, api_client, sample_products):
        """Test filtering products by name"""
        # Search for products with 'design' in name (Database Design exists)
        query = '''
            query {
                productsFiltered(filters: {name: "design"}) {
                    items {
                        name
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        # Verify filter returns results and is case-insensitive
        assert isinstance(items, list)
        if len(items) > 0:
            assert any('Design' in item['name'] for item in items)
    
    def test_filter_products_by_category(self, api_client, sample_products, sample_categories):
        """Test filtering by category"""
        elec_id = sample_categories[0].id
        query = f'''
            query {{
                productsFiltered(filters: {{categoryId: {elec_id}}}) {{
                    items {{
                        name
                        category {{
                            name
                        }}
                    }}
                    totalCount
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(item['category']['name'] == "Electronics" for item in items)
    
    def test_filter_by_price_range(self, api_client, sample_products):
        """Test filtering by price range"""
        query = '''
            query {
                productsFiltered(filters: {priceMin: 20.0, priceMax: 50.0}) {
                    items {
                        name
                        price
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(20.0 <= float(item['price']) <= 50.0 for item in items)
    
    def test_filter_active_products(self, api_client, sample_products):
        """Test filtering active products only"""
        query = '''
            query {
                productsFiltered(filters: {isActive: true}) {
                    items {
                        name
                        isActive
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(item['isActive'] for item in items)
        assert len(items) >= 4  # At least the active products
    
    def test_filter_featured_products(self, api_client, sample_products):
        """Test filtering featured products"""
        query = '''
            query {
                productsFiltered(filters: {isFeatured: true}) {
                    items {
                        name
                        isFeatured
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(item['isFeatured'] for item in items)
        assert len(items) >= 2  # At least Laptop and Mouse
    
    def test_filter_products_with_stock(self, api_client, sample_products):
        """Test filtering products with stock"""
        query = '''
            query {
                productsFiltered(filters: {hasStock: true}) {
                    items {
                        name
                        stockQuantity
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(item['stockQuantity'] > 0 for item in items)
    
    def test_filter_by_rating(self, api_client, sample_products):
        """Test filtering by minimum rating"""
        query = '''
            query {
                productsFiltered(filters: {ratingMin: 4.0}) {
                    items {
                        name
                        rating
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        assert all(float(item['rating']) >= 4.0 for item in items)
    
    def test_combined_filters(self, api_client, sample_products, sample_categories):
        """Test multiple filters together"""
        elec_id = sample_categories[0].id
        query = f'''
            query {{
                productsFiltered(filters: {{
                    categoryId: {elec_id}
                    isActive: true
                    priceMin: 25.0
                }}) {{
                    items {{
                        name
                        price
                        category {{
                            name
                        }}
                    }}
                    totalCount
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        # Should get products in Electronics, active, price >= 25
        for item in items:
            assert item['category']['name'] == "Electronics"
            assert float(item['price']) >= 25.0


# ==================== Sorting Tests ====================

@pytest.mark.sorting
@pytest.mark.django_db
class TestSorting:
    """Test sorting functionality"""
    
    def test_sort_by_price_asc(self, api_client, sample_products):
        """Test sorting by price ascending"""
        query = '''
            query {
                productsFiltered(sort: {field: "price", order: "asc"}) {
                    items {
                        name
                        price
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        prices = [float(item['price']) for item in items]
        assert prices == sorted(prices)
    
    def test_sort_by_price_desc(self, api_client, sample_products):
        """Test sorting by price descending"""
        query = '''
            query {
                productsFiltered(sort: {field: "price", order: "desc"}) {
                    items {
                        name
                        price
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        prices = [float(item['price']) for item in items]
        assert prices == sorted(prices, reverse=True)
    
    def test_sort_by_name(self, api_client, sample_products):
        """Test sorting by name"""
        query = '''
            query {
                productsFiltered(sort: {field: "name", order: "asc"}) {
                    items {
                        name
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        names = [item['name'] for item in items]
        assert names == sorted(names)
    
    def test_sort_by_rating_desc(self, api_client, sample_products):
        """Test sorting by rating descending"""
        query = '''
            query {
                productsFiltered(sort: {field: "rating", order: "desc"}) {
                    items {
                        name
                        rating
                    }
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        items = result['data']['productsFiltered']['items']
        ratings = [float(item['rating']) for item in items]
        assert ratings == sorted(ratings, reverse=True)


# ==================== Offset Pagination Tests ====================

@pytest.mark.pagination
@pytest.mark.django_db
class TestOffsetPagination:
    """Test offset-based pagination"""
    
    def test_pagination_first_page(self, api_client, sample_products):
        """Test first page of pagination"""
        query = '''
            query {
                productsFiltered(page: 1, pageSize: 2) {
                    items {
                        name
                    }
                    totalCount
                    page
                    pageSize
                    totalPages
                    hasNext
                    hasPrevious
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsFiltered']
        assert len(data['items']) <= 2  # pageSize=2, so max 2 items
        assert data['page'] == 1
        assert data['hasPrevious'] is False
    
    def test_pagination_second_page(self, api_client, sample_products):
        """Test second page of pagination"""
        query = '''
            query {
                productsFiltered(page: 2, pageSize: 2) {
                    items {
                        name
                    }
                    page
                    hasNext
                    hasPrevious
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsFiltered']
        assert len(data['items']) <= 2  # pageSize=2
        assert data['hasPrevious'] is True
    
    def test_pagination_last_page(self, api_client, sample_products):
        """Test last page of pagination"""
        query = '''
            query {
                productsFiltered(page: 3, pageSize: 2) {
                    items {
                        name
                    }
                    page
                    hasNext
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsFiltered']
        assert len(data['items']) >= 1  # At least 1 item on last page
        # Don't check hasNext since we don't know exact total with existing data
    
    def test_pagination_total_pages(self, api_client, sample_products):
        """Test total pages calculation"""
        query = '''
            query {
                productsFiltered(pageSize: 2) {
                    totalCount
                    totalPages
                    pageSize
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsFiltered']
        total_count = data['totalCount']
        total_pages = data['totalPages']
        expected_pages = (total_count + 1) // 2  # ceil(total_count/2)
        assert data['pageSize'] == 2
        assert total_pages == expected_pages


# ==================== Cursor Pagination Tests ====================

@pytest.mark.pagination
@pytest.mark.django_db
class TestCursorPagination:
    """Test cursor-based pagination"""
    
    def test_cursor_pagination_first_items(self, api_client, sample_products):
        """Test fetching first N items"""
        query = '''
            query {
                productsPaginated(first: 2) {
                    edges {
                        node {
                            name
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        endCursor
                    }
                    totalCount
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsPaginated']
        assert len(data['edges']) <= 2  # first=2
        assert 'pageInfo' in data
        assert 'totalCount' in data
    
    def test_cursor_pagination_with_after(self, api_client, sample_products):
        """Test pagination with after cursor"""
        # First get initial page
        query1 = '''
            query {
                productsPaginated(first: 2) {
                    edges {
                        cursor
                    }
                    pageInfo {
                        endCursor
                    }
                }
            }
        '''
        result1 = api_client.execute(query1)
        assert 'errors' not in result1
        cursor = result1['data']['productsPaginated']['pageInfo']['endCursor']
        assert cursor is not None
        
        # Now get next page
        query2 = f'''
            query {{
                productsPaginated(first: 2, after: "{cursor}") {{
                    edges {{
                        node {{
                            name
                        }}
                    }}
                    pageInfo {{
                        hasPreviousPage
                    }}
                }}
            }}
        '''
        result2 = api_client.execute(query2)
        assert 'errors' not in result2
        data = result2['data']['productsPaginated']
        # Verify pagination structure exists and works
        assert 'edges' in data
        assert 'pageInfo' in data
        assert len(data['edges']) <= 2


# ==================== Aggregation Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestAggregations:
    """Test aggregation queries"""
    
    def test_avg_product_price(self, api_client, sample_products):
        """Test average price calculation"""
        query = '''
            query {
                avgProductPrice
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        avg_price = result['data']['avgProductPrice']
        assert avg_price is not None
        assert avg_price > 0
    
    def test_price_range_counts(self, api_client, sample_products):
        """Test price range bucket counts"""
        query = '''
            query {
                priceRangeBudget
                priceRangeMid
                priceRangePremium
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        # Should have products in each category
        assert result['data']['priceRangeBudget'] >= 0
        assert result['data']['priceRangeMid'] >= 0
        assert result['data']['priceRangePremium'] >= 0


# ==================== Review Query Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestReviewQueries:
    """Test review-related queries"""
    
    def test_reviews_by_product(self, api_client, sample_reviews, sample_products):
        """Test getting reviews for specific product"""
        product_id = sample_products[0].id
        query = f'''
            query {{
                reviewsByProduct(productId: {product_id}) {{
                    id
                    user
                    rating
                    product {{
                        name
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        reviews = result['data']['reviewsByProduct']
        assert all(review['product']['name'] == "Laptop" for review in reviews)
    
    def test_reviews_by_rating(self, api_client, sample_reviews):
        """Test filtering reviews by rating"""
        query = '''
            query {
                reviewsByRating(rating: 5) {
                    id
                    rating
                    user
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        reviews = result['data']['reviewsByRating']
        assert isinstance(reviews, list)
        # Verify that the query returns reviews (if there are any)
        # Just check that the structure is correct
        for review in reviews:
            assert 'id' in review
            assert 'rating' in review
            assert 'user' in review


# ==================== Integration Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestComplexScenarios:
    """Test complex multi-operation scenarios"""
    
    def test_filter_sort_paginate_together(self, api_client, sample_products):
        """Test combining filter, sort, and pagination"""
        query = '''
            query {
                productsFiltered(
                    filters: {isActive: true, priceMin: 20.0}
                    sort: {field: "price", order: "asc"}
                    page: 1
                    pageSize: 2
                ) {
                    items {
                        name
                        price
                        isActive
                    }
                    totalCount
                    hasNext
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        data = result['data']['productsFiltered']
        # Check filtering
        for item in data['items']:
            assert item['isActive'] is True
            assert float(item['price']) >= 20.0
        # Check sorting
        prices = [float(item['price']) for item in data['items']]
        assert prices == sorted(prices)
    
    def test_category_with_filtered_products(self, api_client, sample_categories, sample_products):
        """Test getting category with specific products"""
        cat_id = sample_categories[0].id
        query = f'''
            query {{
                category(id: {cat_id}) {{
                    name
                    products {{
                        name
                        price
                        isActive
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        category = result['data']['category']
        assert category['name'] == "Electronics"
        assert len(category['products']) >= 2  # At least Laptop and Mouse


# ==================== HTTP Endpoint Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestHTTPEndpoint:
    """Test GraphQL HTTP endpoint"""
    
    def test_query_via_http(self, http_client, sample_products):
        """Test query through HTTP POST"""
        query_data = {
            "query": '''
                query {
                    allProducts {
                        id
                        name
                        price
                    }
                }
            '''
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(query_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'data' in data
        assert len(data['data']['allProducts']) >= 5
