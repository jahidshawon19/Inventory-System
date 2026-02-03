from django.contrib import admin
from .models import Product, Issue, Return

# =============================
# Product Admin
# =============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'quantity', 'total_price', 'created_date', 'is_low_stock')
    list_filter = ('created_date',)
    search_fields = ('name',)
    readonly_fields = ('total_price', 'created_date')
    list_per_page = 20  # pagination in admin

    # Highlight low stock products
    def is_low_stock(self, obj):
        return obj.quantity <= 5
    is_low_stock.boolean = True  # shows as a green checkmark in admin
    is_low_stock.short_description = 'Low Stock?'


# =============================
# Issue Admin
# =============================
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'issued_quantity', 'issued_date')
    list_filter = ('issued_date', 'product')
    search_fields = ('product__name',)
    readonly_fields = ('issued_date',)
    list_per_page = 20


# =============================
# Return Admin
# =============================
@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'return_quantity', 'return_date')
    list_filter = ('return_date', 'product')
    search_fields = ('product__name',)
    readonly_fields = ('return_date',)
    list_per_page = 20
