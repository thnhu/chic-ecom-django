from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Product, Customer, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CustomerSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

# Abstract base class for common API view behavior
class BaseAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        abstract = True

# Customer Registration
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Customer Login
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_customer(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Customer Logout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_customer(request):
    logout(request)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

# Admin Login (assuming admin inherits from Customer model)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_admin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user and user.is_staff:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid admin credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Admin Logout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_admin(request):
    logout(request)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

# List Products (Homepage)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# Product Detail
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# Add Product to Cart
class AddToCartView(BaseAPIView):
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        serializer = self.serializer_class(data={**request.data, 'cart': cart.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Buy Now (Direct Order Creation)
class BuyNowView(BaseAPIView):
    serializer_class = OrderSerializer

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id, is_available=True)
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        order_data = {
            'customer': request.user.customer.id,
            'total_amount': product.price,
            'items': [{'product': product.id, 'quantity': 1, 'price': product.price}]
        }
        serializer = self.serializer_class(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Search Products
class SearchProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )

# Create Order from Cart
class CreateOrderFromCartView(BaseAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer=request.user.customer, is_active=True)
        total_amount = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        order_data = {
            'customer': request.user.customer.id,
            'total_amount': total_amount,
            'items': [{'product': item.product.id, 'quantity': item.quantity, 'price': item.product.price} for item in cart.cartitem_set.all()]
        }
        serializer = self.serializer_class(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            cart.cartitem_set.all().delete()
            cart.is_active = False
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Review (Update Order Details)
class OrderReviewView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Order.objects.get(id=self.kwargs['pk'], customer=self.request.user.customer)

# Admin Manage Orders
class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin Manage Products
class AdminProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin Manage Customers
class AdminCustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin Manage Inventory
class AdminInventoryListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]