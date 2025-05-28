from rest_framework import serializers
from .models import Product, Order, OrderItem
from django.db import transaction
from .services import OrderService

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["user", "order_items", "total_price", "created_at"]
        read_only_fields = ["created_at"]

    def get_total_price(self, obj):
        return obj.total_price

    def create(self, validated_data):
        return OrderService.create_order(validated_data)

    def update(self, instance, validated_data):
        return OrderService.update_order(instance, validated_data)