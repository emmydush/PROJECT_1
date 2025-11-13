from django.core.management.base import BaseCommand
from products.models import Category, Unit, Product
from customers.models import Customer
from suppliers.models import Supplier
from superadmin.models import Business
from decimal import Decimal
import random
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample data including 20 products, 20 customers, and 20 suppliers'

    def add_arguments(self, parser):
        parser.add_argument('--business-id', type=int, required=True, help='ID of the business to create data for')

    def handle(self, *args, **options):
        business_id = options['business_id']
        
        try:
            business = Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Business with ID {business_id} does not exist')
            )
            return

        # Create or get categories and units using a more robust approach
        # Use for_business to bypass current business context filtering
        existing_categories = list(Category.objects.for_business(business))
        self.stdout.write(f'Found {len(existing_categories)} existing categories')
        
        # Create categories if we don't have enough
        if len(existing_categories) < 8:
            categories_data = [
                {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
                {'name': 'Clothing', 'description': 'Apparel and fashion items'},
                {'name': 'Food & Beverages', 'description': 'Food products and drinks'},
                {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
                {'name': 'Books', 'description': 'Books and educational materials'},
                {'name': 'Sports', 'description': 'Sports equipment and accessories'},
                {'name': 'Beauty', 'description': 'Beauty and personal care products'},
                {'name': 'Toys', 'description': 'Toys and games for children'},
            ]
            
            for cat_data in categories_data:
                # Always try to create, and handle the exception if it already exists
                try:
                    category = Category.objects.for_business(business).create(
                        business=business,
                        name=cat_data['name'],
                        description=cat_data['description']
                    )
                    existing_categories.append(category)
                    self.stdout.write(f'Created category: {category.name}')
                except Exception as e:
                    # If it already exists, get it
                    try:
                        category = Category.objects.for_business(business).get(name=cat_data['name'])
                        existing_categories.append(category)
                        self.stdout.write(f'Using existing category: {category.name}')
                    except Category.DoesNotExist:
                        self.stdout.write(f'Could not create or find category {cat_data["name"]}: {e}')
        
        # Make sure we have at least one category
        if not existing_categories:
            # Create a default category
            try:
                default_category = Category.objects.for_business(business).create(
                    business=business,
                    name='General',
                    description='General products'
                )
                existing_categories.append(default_category)
                self.stdout.write(f'Created default category: {default_category.name}')
            except Exception as e:
                self.stdout.write(f'Error creating default category: {e}')
                return

        # Create or get units
        existing_units = list(Unit.objects.for_business(business))
        self.stdout.write(f'Found {len(existing_units)} existing units')
        
        # Create units if we don't have enough
        if len(existing_units) < 6:
            units_data = [
                {'name': 'Piece', 'symbol': 'pc'},
                {'name': 'Kilogram', 'symbol': 'kg'},
                {'name': 'Liter', 'symbol': 'L'},
                {'name': 'Box', 'symbol': 'box'},
                {'name': 'Pack', 'symbol': 'pack'},
                {'name': 'Meter', 'symbol': 'm'},
            ]
            
            for unit_data in units_data:
                # Always try to create, and handle the exception if it already exists
                try:
                    unit = Unit.objects.for_business(business).create(
                        business=business,
                        name=unit_data['name'],
                        symbol=unit_data['symbol']
                    )
                    existing_units.append(unit)
                    self.stdout.write(f'Created unit: {unit.name}')
                except Exception as e:
                    # If it already exists, get it
                    try:
                        unit = Unit.objects.for_business(business).get(name=unit_data['name'])
                        existing_units.append(unit)
                        self.stdout.write(f'Using existing unit: {unit.name}')
                    except Unit.DoesNotExist:
                        self.stdout.write(f'Could not create or find unit {unit_data["name"]}: {e}')
        
        # Make sure we have at least one unit
        if not existing_units:
            # Create a default unit
            try:
                default_unit = Unit.objects.for_business(business).create(
                    business=business,
                    name='Unit',
                    symbol='unit'
                )
                existing_units.append(default_unit)
                self.stdout.write(f'Created default unit: {default_unit.name}')
            except Exception as e:
                self.stdout.write(f'Error creating default unit: {e}')
                return

        # Create 20 products
        product_names = [
            'Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch',
            'T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress',
            'Coffee Beans', 'Energy Drink', 'Chocolate Bar', 'Protein Powder', 'Vitamin Supplements',
            'Garden Tools Set', 'Fertilizer', 'Plant Seeds', 'Watering Can', 'Gloves'
        ]
        
        for i in range(20):
            # Ensure we have categories and units to work with
            category = existing_categories[i % len(existing_categories)] if existing_categories else None
            unit = existing_units[i % len(existing_units)] if existing_units else None
            
            if not category or not unit:
                self.stdout.write(self.style.ERROR('No categories or units available'))
                return
                
            # Generate a unique SKU for this business
            base_sku = f'PRD{i+1:03d}'
            sku = f'{base_sku}-B{business_id}'  # Make SKU unique per business
            
            product_data = {
                'business': business,
                'name': f'{product_names[i % len(product_names)]} {i+1}',  # Make names unique
                'sku': sku,
                'category': category,
                'unit': unit,
                'description': f'Description for {product_names[i % len(product_names)]} {i+1}',
                'cost_price': Decimal(random.uniform(10, 200)).quantize(Decimal('0.01')),
                'selling_price': Decimal(random.uniform(20, 300)).quantize(Decimal('0.01')),
                'quantity': Decimal(random.uniform(5, 100)).quantize(Decimal('0.01')),
                'reorder_level': Decimal(random.uniform(1, 20)).quantize(Decimal('0.01')),
            }
            
            # Check if product already exists
            if not Product.objects.for_business(business).filter(sku=product_data['sku']).exists():
                try:
                    product = Product.objects.for_business(business).create(**product_data)
                    self.stdout.write(f'Created product: {product.name}')
                except Exception as e:
                    self.stdout.write(f'Error creating product {product_data["name"]}: {e}')
            else:
                try:
                    product = Product.objects.for_business(business).get(sku=product_data['sku'])
                    self.stdout.write(f'Using existing product: {product.name}')
                except Exception as e:
                    self.stdout.write(f'Error getting existing product {product_data["sku"]}: {e}')

        # Create 20 customers
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David',
            'Emily', 'Robert', 'Lisa', 'William', 'Jennifer',
            'Thomas', 'Mary', 'Charles', 'Patricia', 'Daniel',
            'Linda', 'Matthew', 'Elizabeth', 'Anthony', 'Barbara'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
            'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
            'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'
        ]
        
        for i in range(20):
            # Make email unique per business
            email = f'{first_names[i].lower()}.{last_names[i].lower()}{i+1}.b{business_id}@example.com'
            
            customer_data = {
                'business': business,
                'first_name': first_names[i],
                'last_name': last_names[i],
                'email': email,
                'phone': f'+1-555-{random.randint(1000, 9999)}',
                'address': f'{random.randint(100, 999)} Main Street, City {i+1}',
                'company': f'Company {i+1}',
                'loyalty_points': Decimal(random.uniform(0, 1000)).quantize(Decimal('0.01')),
                'credit_limit': Decimal(random.uniform(0, 5000)).quantize(Decimal('0.01')),
            }
            
            # Check if customer already exists
            if not Customer.objects.for_business(business).filter(email=customer_data['email']).exists():
                try:
                    customer = Customer.objects.for_business(business).create(**customer_data)
                    self.stdout.write(f'Created customer: {customer.full_name}')
                except Exception as e:
                    self.stdout.write(f'Error creating customer {customer_data["first_name"]} {customer_data["last_name"]}: {e}')
            else:
                try:
                    customer = Customer.objects.for_business(business).get(email=customer_data['email'])
                    self.stdout.write(f'Using existing customer: {customer.full_name}')
                except Exception as e:
                    self.stdout.write(f'Error getting existing customer {customer_data["email"]}: {e}')

        # Create 20 suppliers
        supplier_names = [
            'Tech Solutions Inc.', 'Fashion Hub Ltd.', 'Food Distributors Co.', 'Garden Supplies Corp.',
            'Book Publishers LLC', 'Sports Equipment Inc.', 'Beauty Products Ltd.', 'Toy Manufacturers Co.',
            'Electronics Wholesalers', 'Clothing Suppliers Ltd.', 'Beverage Distributors Inc.',
            'Home Improvement Supplies', 'Educational Materials Co.', 'Fitness Gear Ltd.',
            'Personal Care Products', 'Children\'s Products Inc.', 'Appliance Suppliers',
            'Office Equipment Co.', 'Automotive Parts Ltd.', 'Hardware Distributors'
        ]
        
        for i in range(20):
            # Make supplier name unique per business
            supplier_name = f'{supplier_names[i % len(supplier_names)]} {i+1} (B{business_id})'
            
            supplier_data = {
                'business': business,
                'name': supplier_name,
                'email': f'info{i+1}.b{business_id}@{supplier_names[i % len(supplier_names)].replace(" ", "").replace(".", "").replace("\'", "").lower()}.com',
                'phone': f'+1-555-{random.randint(1000, 9999)}',
                'address': f'{random.randint(1000, 9999)} Industrial Blvd, Business Park {i+1}',
                'company': f'{supplier_names[i % len(supplier_names)]} {i+1}',
                'contact_person': f'{random.choice(first_names)} {random.choice(last_names)}',
                'contact_person_phone': f'+1-555-{random.randint(1000, 9999)}',
                'contact_person_email': f'{random.choice(first_names).lower()}.{random.choice(last_names).lower()}{i+1}.b{business_id}@{supplier_names[i % len(supplier_names)].replace(" ", "").replace(".", "").replace("\'", "").lower()}.com',
            }
            
            # Check if supplier already exists
            if not Supplier.objects.for_business(business).filter(name=supplier_data['name']).exists():
                try:
                    supplier = Supplier.objects.for_business(business).create(**supplier_data)
                    self.stdout.write(f'Created supplier: {supplier.name}')
                except Exception as e:
                    self.stdout.write(f'Error creating supplier {supplier_data["name"]}: {e}')
            else:
                try:
                    supplier = Supplier.objects.for_business(business).get(name=supplier_data['name'])
                    self.stdout.write(f'Using existing supplier: {supplier.name}')
                except Exception as e:
                    self.stdout.write(f'Error getting existing supplier {supplier_data["name"]}: {e}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data for business "{business.company_name}"'
            )
        )