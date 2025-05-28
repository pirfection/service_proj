import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
import jwt


logger = logging.getLogger(__name__)


def get_user_from_token(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            payload = jwt.decode(
                token, "fnwalfwjfbjkfnwalfkjadihbvaboda", algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            from django.contrib.auth import get_user_model

            User = get_user_model()
            return User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except User.DoesNotExist:
            return None
    return None


class SubscriptionCheckMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path == "/api/orders/":
            user = get_user_from_token(request)
            if user is not None:
                if not self.has_active_subscription(user):
                    logger.warning(
                        f"SubscriptionCheckMiddleware: User {user.username} has no active subscription."
                    )
                    return HttpResponseForbidden(
                        "У вас нет активной подписки для создания заказов."
                    )
            else:
                logger.warning(
                    "SubscriptionCheckMiddleware: Invalid JWT or no JWT provided."
                )
                return HttpResponseForbidden(
                    "Вы должны быть авторизованы для создания заказов."
                )

        response = self.get_response(request)
        return response

    def has_active_subscription(self, user):
        return user.subscriptions.exists()
