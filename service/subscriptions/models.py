from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="telegram_profile"
    )
    telegram_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.telegram_id}"


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    time_start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tariff.name}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
