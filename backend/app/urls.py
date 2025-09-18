from django.urls import path
from . import views

urlpatterns = [
    # Customer Authentication
    path('register/', views.register_customer, name='register_customer'),
    path('login/', views.login_customer, name='login_customer'),
    path('logout/', views.logout_customer, name='logout_customer'),

    # Admin Authentication
    path('admin/login/', views.login_admin, name='login_admin'),
    path('admin/logout/', views.logout_admin, name='logout_admin'),

    # Product Endpoints
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/search/', views.SearchProductView.as_view(), name='search_products'),

    # Cart Endpoints
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/order/', views.CreateOrderFromCartView.as_view(), name='create_order_from_cart'),

    # Buy Now Endpoint
    path('buy/<int:product_id>/', views.BuyNowView.as_view(), name='buy_now'),

    # Order Endpoints
    path('orders/<int:pk>/review/', views.OrderReviewView.as_view(), name='order_review'),

    # Admin Management Endpoints
    path('admin/orders/', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/products/', views.AdminProductListView.as_view(), name='admin_product_list'),
    path('admin/customers/', views.AdminCustomerListView.as_view(), name='admin_customer_list'),
    path('admin/inventory/', views.AdminInventoryListView.as_view(), name='admin_inventory_list'),
]