from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

from .permissions import IsOwnerOrAdminorReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related("order_items")
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdminorReadOnly]

    def perform_create(self, serializer):
        if self.request.user.id != serializer.validated_data["user"].id:
            raise PermissionError
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.id != serializer.validated_data["user"].id:
            raise PermissionError
        serializer.save(user=self.request.user)
