from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q
from django.db import transaction
import json
import datetime

from .models import Medicine, Category, Stock, Sale, SaleItem
from .forms import LoginForm, MedicineForm, StockForm, SaleForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'pos/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Basic stats for dashboard
    total_medicines = Medicine.objects.count()
    low_stock_count = Stock.objects.filter(quantity__lt=10).count()
    expired_count = Stock.objects.filter(expiry_date__lt=timezone.now().date()).count()
    
    # Today's sales
    today = timezone.now().date()
    today_sales = Sale.objects.filter(timestamp__date=today)
    today_amount = today_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'total_medicines': total_medicines,
        'low_stock_count': low_stock_count,
        'expired_count': expired_count,
        'today_sales_count': today_sales.count(),
        'today_amount': today_amount,
    }
    return render(request, 'pos/dashboard.html', context)


@login_required
def inventory(request):
    medicines = Medicine.objects.all()
    stocks = Stock.objects.all().order_by('medicine__name', '-date_added')
    
    return render(request, 'pos/inventory.html', {
        'medicines': medicines,
        'stocks': stocks,
    })


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine added successfully!")
            return redirect('inventory')
    else:
        form = MedicineForm()
    
    return render(request, 'pos/add_medicine.html', {'form': form})


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock added successfully!")
            return redirect('inventory')
    else:
        form = StockForm()
    
    return render(request, 'pos/add_stock.html', {'form': form})


@login_required
def pos(request):
    medicines = Medicine.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'pos/pos.html', {
        'medicines': medicines,
        'categories': categories,
    })


@login_required
def get_medicine_details(request, medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id)
        # Get available stock
        available_stock = Stock.objects.filter(
            medicine=medicine,
            quantity__gt=0,
            expiry_date__gt=timezone.now().date()
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        return JsonResponse({
            'id': medicine.id,
            'name': medicine.name,
            'price': float(medicine.price),
            'available': available_stock,
        })
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)


@login_required
@transaction.atomic
def create_sale(request):
    if request.method == 'POST':
        try:
            # Handle both form data and JSON data
            if request.content_type and 'application/json' in request.content_type:
                data = json.loads(request.body)
            else:
                # Try to parse the body as JSON anyway (for flexibility)
                try:
                    data = json.loads(request.body)
                except:
                    # Fall back to POST data
                    data = request.POST
            
            items = data.get('items', [])
            total_amount = data.get('total')
            payment_method = data.get('payment_method')
            
            if not items:
                return JsonResponse({'error': 'No items in cart'}, status=400)
            
            # Convert items to list if it's a string
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except:
                    return JsonResponse({'error': 'Invalid items format'}, status=400)
                
            # Create sale
            sale = Sale.objects.create(
                total_amount=total_amount,
                payment_method=payment_method,
                cashier=request.user
            )
            
            # Add sale items and update stock
            for item in items:
                medicine = Medicine.objects.get(id=item['id'])
                quantity = item['quantity']
                price = item['price']
                
                SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    quantity=quantity,
                    price=price
                )
                
                # Update stock (FIFO)
                remaining = quantity
                stocks = Stock.objects.filter(
                    medicine=medicine,
                    quantity__gt=0,
                    expiry_date__gt=timezone.now().date()
                ).order_by('expiry_date')
                
                for stock in stocks:
                    if remaining <= 0:
                        break
                        
                    if stock.quantity >= remaining:
                        stock.quantity -= remaining
                        remaining = 0
                    else:
                        remaining -= stock.quantity
                        stock.quantity = 0
                    
                    stock.save()
                
                if remaining > 0:
                    # Rollback transaction
                    transaction.set_rollback(True)
                    return JsonResponse({'error': f'Not enough stock for {medicine.name}'}, status=400)
            
            return JsonResponse({'success': True, 'sale_id': sale.id})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # Rollback transaction
            transaction.set_rollback(True)
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def sales_history(request):
    sales = Sale.objects.all().order_by('-timestamp')
    return render(request, 'pos/sales_history.html', {'sales': sales})


@login_required
def sale_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()
    
    return render(request, 'pos/sale_detail.html', {
        'sale': sale,
        'items': items,
    })