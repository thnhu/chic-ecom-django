from rest_framework import serializers
from .models import Product, Customer, Cart, CartItem, Order, OrderItem
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'description', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']  # Bỏ 'password' ở đây
        extra_kwargs = {
            'password': {'write_only': True}  # Chỉ input, không output
        }

    def create(self, validated_data):
        # Override create để hash password ngay khi save (tốt hơn update sau)
        validated_data['password'] = make_password(validated_data.pop('password'))
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if Customer.objects.filter(email=email).exists():
            customer = Customer.objects.get(email=email)
            if not check_password(password, customer.password):
                raise serializers.ValidationError("Sai mật khẩu!")
        else:
            raise serializers.ValidationError("Email không tồn tại!")

        data['customer'] = customer
        return data

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        cart = validated_data['cart']
        product, _ = Product.objects.get_or_create(**product_data)
        cart_item = CartItem.objects.create(cart=cart, product=product, **validated_data)
        return cart_item

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        order = validated_data['order']
        product, _ = Product.objects.get_or_create(**product_data)
        order_item = OrderItem.objects.create(order=order, product=product, **validated_data)
        return order_item

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItemSerializer().create({**item_data, 'order': order})
        return order