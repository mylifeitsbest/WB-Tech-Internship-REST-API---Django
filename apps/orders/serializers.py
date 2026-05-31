from rest_framework import serializers
from .models import CartItem, Order, OrderItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_details', 'quantity')

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество товара должно быть больше 0.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'status', 'created_at', 'items')
