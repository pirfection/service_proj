from rest_framework import serializers
from .models import Tariff, UserSubscription
from django.contrib.auth import get_user_model

User = get_user_model()


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ["id", "name", "price", "description"]


class UserSubscriptionSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tariff_id = serializers.PrimaryKeyRelatedField(
        source="tariff", queryset=Tariff.objects.all()
    )
    tariff_name = serializers.ReadOnlyField(source="tariff.name")
    time_start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserSubscription
        fields = ["id", "user", "tariff_id", "tariff_name", "time_start"]
        read_only_fields = ["tariff_name"]
