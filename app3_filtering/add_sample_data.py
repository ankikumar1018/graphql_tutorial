"""
Script to populate App 3 with sample data.

Run this after migrations:
python manage.py shell < add_sample_data.py
"""

import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from filtering_app.models import Category, Product, Review

# Clear existing data
Review.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

print("Creating categories...")

# Create categories
electronics = Category.objects.create(
    name='Electronics',
    slug='electronics',
    description='Electronic devices and gadgets'
)

books = Category.objects.create(
    name='Books',
    slug='books',
    description='Books and literature'
)

clothing = Category.objects.create(
    name='Clothing',
    slug='clothing',
    description='Apparel and fashion'
)

home = Category.objects.create(
    name='Home & Garden',
    slug='home-garden',
    description='Home and garden supplies'
)

print("Creating products...")

# Create products with various details
products_data = [
    # Electronics
    ('Laptop Pro', 'laptop-pro', 'High-performance laptop', electronics, Decimal('1299.99'), 10, 'LAPTOP001', True, True, 4.5, 120),
    ('Wireless Mouse', 'wireless-mouse', 'Ergonomic wireless mouse', electronics, Decimal('49.99'), 0, 'MOUSE001', False, True, 4.2, 85),
    ('USB-C Cable', 'usb-c-cable', '2-meter USB-C charging cable', electronics, Decimal('19.99'), 20, 'CABLE001', False, True, 4.8, 200),
    ('4K Monitor', '4k-monitor', '27-inch 4K ultra HD display', electronics, Decimal('599.99'), 5, 'MONITOR001', True, True, 4.7, 95),
    ('Mechanical Keyboard', 'mech-keyboard', 'RGB mechanical gaming keyboard', electronics, Decimal('149.99'), 15, 'KEYBOARD001', True, True, 4.9, 340),
    
    # Books
    ('Python Programming', 'python-programming', 'Complete guide to Python', books, Decimal('59.99'), 30, 'BOOK001', True, True, 4.6, 250),
    ('GraphQL Guide', 'graphql-guide', 'Mastering GraphQL APIs', books, Decimal('49.99'), 20, 'BOOK002', True, True, 4.8, 180),
    ('Web Development', 'web-development', 'Full-stack web development', books, Decimal('79.99'), 0, 'BOOK003', False, False, 4.3, 150),
    ('Database Design', 'database-design', 'Advanced database design patterns', books, Decimal('89.99'), 10, 'BOOK004', False, True, 4.7, 95),
    
    # Clothing
    ('Cotton T-Shirt', 'cotton-tshirt', '100% organic cotton t-shirt', clothing, Decimal('24.99'), 50, 'SHIRT001', False, True, 4.4, 200),
    ('Jeans', 'blue-jeans', 'Classic blue denim jeans', clothing, Decimal('64.99'), 35, 'JEANS001', False, True, 4.5, 300),
    ('Winter Jacket', 'winter-jacket', 'Waterproof winter jacket', clothing, Decimal('199.99'), 8, 'JACKET001', True, True, 4.6, 120),
    ('Sneakers', 'running-sneakers', 'Comfortable running shoes', clothing, Decimal('129.99'), 12, 'SHOES001', True, True, 4.7, 280),
    
    # Home
    ('Coffee Maker', 'coffee-maker', 'Programmable coffee machine', home, Decimal('99.99'), 20, 'COFFEE001', True, True, 4.5, 150),
    ('Bed Sheets', 'bed-sheets', 'Egyptian cotton bed sheets', home, Decimal('44.99'), 40, 'SHEETS001', False, True, 4.8, 320),
    ('Desk Lamp', 'desk-lamp', 'LED desk lamp with USB charging', home, Decimal('39.99'), 25, 'LAMP001', False, True, 4.3, 110),
    ('Plant Pot', 'ceramic-pot', 'Decorative ceramic plant pot', home, Decimal('34.99'), 60, 'POT001', False, True, 4.2, 95),
]

products = []
for name, slug, desc, cat, price, stock, sku, featured, active, rating, reviews in products_data:
    product = Product.objects.create(
        name=name,
        slug=slug,
        description=desc,
        category=cat,
        price=price,
        stock_quantity=stock,
        sku=sku,
        is_featured=featured,
        is_active=active,
        rating=Decimal(str(rating)),
        review_count=reviews,
        published_date=datetime.now().date() - timedelta(days=30)
    )
    products.append(product)

print("Creating reviews...")

# Create reviews
review_data = [
    (products[0], 'john_doe', 5, 'Excellent laptop', 'Best laptop I have ever used. Highly recommended!', True, 45),
    (products[0], 'jane_smith', 4, 'Good but expensive', 'Great performance but the price is steep', True, 35),
    (products[2], 'tech_guy', 5, 'Perfect cable', 'Excellent quality and length', False, 20),
    (products[4], 'gamer_pro', 5, 'Gaming perfection', 'Best keyboard for gaming, amazing tactile feedback', True, 120),
    (products[5], 'python_dev', 5, 'Fantastic resource', 'Comprehensive and easy to follow', True, 80),
    (products[6], 'api_expert', 5, 'Must read', 'The best guide to GraphQL available', True, 65),
    (products[9], 'fashion_icon', 4, 'Good quality', 'Comfortable and durable t-shirt', False, 30),
    (products[10], 'casual_wear', 5, 'Perfect fit', 'These jeans are amazing', True, 95),
    (products[12], 'shoe_lover', 5, 'Very comfortable', 'My feet feel great in these shoes', True, 110),
    (products[14], 'coffee_addict', 4, 'Great coffee', 'Makes excellent coffee every morning', True, 55),
]

for product, user, rating, title, comment, verified, helpful in review_data:
    Review.objects.create(
        product=product,
        user=user,
        rating=rating,
        title=title,
        comment=comment,
        is_verified_purchase=verified,
        helpful_count=helpful
    )

print("✅ Sample data created successfully!")
print(f"Created {Category.objects.count()} categories")
print(f"Created {Product.objects.count()} products")
print(f"Created {Review.objects.count()} reviews")
