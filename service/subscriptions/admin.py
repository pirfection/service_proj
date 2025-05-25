from django.contrib import admin
from .models import Tariff, UserSubscription, User, TelegramUser


admin.site.register(TelegramUser)
admin.site.register(User)
admin.site.register(Tariff)
admin.site.register(UserSubscription)
