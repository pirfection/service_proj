import logging
from celery import shared_task
from subscriptions.models import TelegramUser
from telegram import Bot
import asyncio

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "7639893989:AAHKCQRE1ipYCpyTcKE_uyJAmkwUhm5xef4"


@shared_task
def send_telegram_message(user_id, order_id):
    from .models import Order, OrderItem

    try:
        telegram_user = TelegramUser.objects.get(user_id=user_id)
        telegram_id = telegram_user.telegram_id
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            logger.error(f"Order with id {order_id} not found.")
            return
        total_price = order.total_price
        order_items = OrderItem.objects.filter(order=order)
        items_string = "\n".join(
            [f"- {item.product.name} ({item.quantity} шт.)" for item in order_items]
        )
        message = f"Новый заказ №{order_id}!\n"
        message += f"Сумма заказа: {total_price} руб.\n"
        message += "Позиции:\n"
        message += items_string
        bot = Bot("7639893989:AAHKCQRE1ipYCpyTcKE_uyJAmkwUhm5xef4")

        async def send_message_async(bot, chat_id, text):
            await bot.send_message(chat_id=chat_id, text=text)

        asyncio.run(send_message_async(bot, telegram_id, message))
        logger.info(f"Successfully sent message to Telegram user {telegram_id}")
    except TelegramUser.DoesNotExist:
        logger.warning(f"Telegram ID for user {user_id} not found.")
    except Exception as e:
        pass
