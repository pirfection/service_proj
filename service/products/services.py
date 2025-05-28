from django.db import transaction
from .models import Order, OrderItem

class OrderService:
    @staticmethod
    def create_order(validated_data):
        order_items_data = validated_data.pop("order_items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
        return order

    @staticmethod
    def update_order(instance, validated_data):
        order_items_data = validated_data.pop("order_items", [])
        with transaction.atomic():
            instance.order_items.all().delete() 
            instance = Order.objects.update(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)