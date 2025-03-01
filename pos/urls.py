from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inventory/', views.inventory, name='inventory'),
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('pos/', views.pos, name='pos'),
    path('api/medicine/<int:medicine_id>/', views.get_medicine_details, name='get_medicine_details'),
    path('api/sale/create/', views.create_sale, name='create_sale'),
    path('sales/', views.sales_history, name='sales_history'),
    path('sales/<int:sale_id>/', views.sale_detail, name='sale_detail'),
]