from django.db import models
from django.conf import settings
import logging
from .tasks import send_telegram_message

logger = logging.getLogger(__name__)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(
            item.product.price * item.quantity for item in self.order_items.all()
        )

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
            send_telegram_message.delay(self.user_id, self.id)
        return result

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
