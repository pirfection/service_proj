from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TariffSerializer, UserSubscriptionSerializer
from .models import Tariff, UserSubscription
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet


class TariffView(mixins.ListModelMixin, GenericViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class SubscriptionView(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all().select_related("tariff", "user")
    serializer_class = UserSubscriptionSerializer
