from django.urls import include, path

from .views import SubscriptionView, TariffView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subscriptions", SubscriptionView, basename="subscriptions")
router.register("tariffs", TariffView, basename="tariffs")

urlpatterns = [
    path("", include(router.urls)),
]
