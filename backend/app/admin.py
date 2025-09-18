from django.contrib import admin
from .models import Product, Collection, Customer, Cart, CartItem, Order, OrderItem

# Abstract base class for common admin configurations
class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id',)

    class Meta:
        abstract = True

# Admin for Product management
@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_available')

# Admin for Collection management
@admin.register(Collection)
class CollectionAdmin(BaseAdmin):
    list_display = ('id', 'title', 'created_at')
    filter_horizontal = ('products',)
    search_fields = ('title', 'description')

# Admin for Customer management
@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)

# Admin for Cart management
@admin.register(Cart)
class CartAdmin(BaseAdmin):
    list_display = ('id', 'customer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name')

# Admin for CartItem management
@admin.register(CartItem)
class CartItemAdmin(BaseAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name',)

# Admin for Order management
@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name')
    list_editable = ('status',)

# Admin for OrderItem management
@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name',)

# Admin for Inventory management (using Product model)
@admin.register(Product)
class InventoryAdmin(ProductAdmin):
    list_display = ('id', 'name', 'stock', 'is_available', 'created_at')
    list_editable = ('stock', 'is_available')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name',)