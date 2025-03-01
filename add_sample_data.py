import os
import django
import sys
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medshop_pos.settings')
django.setup()

# Import models
from pos.models import Category, Medicine, Stock

print("Adding sample data for Medical Shop POS System")
print("============================================")

# Add categories
print("\nAdding medicine categories...")
categories_data = ["Antibiotics", "Painkillers", "Antacids", "Vitamins", "Cardiac"]
category_objs = {}

for category_name in categories_data:
    # Check if category already exists
    category, created = Category.objects.get_or_create(name=category_name)
    category_objs[category_name] = category
    
    if created:
        print(f"✓ Added category: {category_name}")
    else:
        print(f"✓ Category already exists: {category_name}")

# Add medicines
print("\nAdding medicines...")
medicines_data = [
    {"name": "Amoxicillin 500mg", "category": "Antibiotics", "price": 120.00, "description": "Antibiotic for bacterial infections"},
    {"name": "Paracetamol 650mg", "category": "Painkillers", "price": 25.50, "description": "Common pain reliever and fever reducer"},
    {"name": "Pantoprazole 40mg", "category": "Antacids", "price": 85.75, "description": "Reduces stomach acid production"},
    {"name": "Vitamin D3", "category": "Vitamins", "price": 180.00, "description": "Essential for bone health"},
    {"name": "Atenolol 50mg", "category": "Cardiac", "price": 95.25, "description": "Beta-blocker for heart conditions"},
    {"name": "Ibuprofen 400mg", "category": "Painkillers", "price": 40.50, "description": "Anti-inflammatory pain reliever"},
    {"name": "Cetirizine 10mg", "category": "Antibiotics", "price": 65.30, "description": "Antihistamine for allergies"}
]

medicine_objs = {}

for medicine_data in medicines_data:
    # Check if medicine already exists
    medicine, created = Medicine.objects.get_or_create(
        name=medicine_data['name'],
        defaults={
            'category': category_objs[medicine_data['category']],
            'price': medicine_data['price'],
            'description': medicine_data['description']
        }
    )
    medicine_objs[medicine_data['name']] = medicine
    
    if created:
        print(f"✓ Added medicine: {medicine_data['name']} - ₹{medicine_data['price']} ({medicine_data['category']})")
    else:
        print(f"✓ Medicine already exists: {medicine_data['name']}")

# Add stock
print("\nAdding stock entries...")
stocks_data = [
    {"medicine": "Amoxicillin 500mg", "batch": "AM2023001", "qty": 150, "expiry": "2025-12-31"},
    {"medicine": "Paracetamol 650mg", "batch": "PC2023045", "qty": 200, "expiry": "2025-10-15"},
    {"medicine": "Pantoprazole 40mg", "batch": "PT2023087", "qty": 100, "expiry": "2025-08-20"},
    {"medicine": "Vitamin D3", "batch": "VD2023012", "qty": 80, "expiry": "2026-02-28"},
    {"medicine": "Atenolol 50mg", "batch": "AT2023065", "qty": 120, "expiry": "2025-11-30"},
    {"medicine": "Ibuprofen 400mg", "batch": "IB2023034", "qty": 180, "expiry": "2025-09-22"},
    {"medicine": "Cetirizine 10mg", "batch": "CZ2023078", "qty": 90, "expiry": "2025-07-15"}
]

for stock_data in stocks_data:
    # Parse expiry date
    expiry_date = datetime.strptime(stock_data['expiry'], '%Y-%m-%d').date()
    
    # Check if stock with same batch number already exists
    stock, created = Stock.objects.get_or_create(
        medicine=medicine_objs[stock_data['medicine']],
        batch_number=stock_data['batch'],
        defaults={
            'quantity': stock_data['qty'],
            'expiry_date': expiry_date
        }
    )
    
    if created:
        print(f"✓ Added stock: {stock_data['medicine']} - Batch: {stock_data['batch']} - Qty: {stock_data['qty']} - Expires: {stock_data['expiry']}")
    else:
        print(f"✓ Stock already exists for batch: {stock_data['batch']}")

print("\nAll sample data has been added successfully!")
print("You can now access the system with the following sample data.")