from django.urls import include, path

from .views import OrderViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
