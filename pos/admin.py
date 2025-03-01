from django.contrib import admin
from .models import Medicine, Category, Stock, Sale, SaleItem

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

class StockAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'batch_number', 'quantity', 'expiry_date', 'is_expired')
    list_filter = ('medicine__category', 'expiry_date')
    search_fields = ('medicine__name', 'batch_number')
    date_hierarchy = 'expiry_date'

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'cashier', 'payment_method', 'total_amount')
    list_filter = ('payment_method', 'timestamp')
    search_fields = ('cashier__username',)
    date_hierarchy = 'timestamp'
    inlines = [SaleItemInline]

admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Category)
admin.site.register(Stock, StockAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)