import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from asgiref.sync import sync_to_async
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
django.setup()

from django.conf import settings
from django.apps import apps
from .session import get_db, User as SQLAlchemyUser
from subscriptions.models import TelegramUser
from django.core.exceptions import ObjectDoesNotExist


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет! Отправь свой номер телефона, чтобы зарегистрироваться. "
    )


async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        phone = update.message.text
        db = get_db()
        with db.begin():
            userka = (
                db.query(SQLAlchemyUser).filter(SQLAlchemyUser.phone == phone).first()
            )

        if userka:
            await update.message.reply_text(
                f"Пожалуйста, подождите, идёт регистрация + {userka.id}"
            )
            user_id = int(userka.id)
            User = apps.get_model(settings.AUTH_USER_MODEL)
            try:
                django_user = await sync_to_async(User.objects.get)(pk=user_id)
            except ObjectDoesNotExist:
                await update.message.reply_text(
                    "Пользователь не найден в системе Django."
                )
                return

            try:
                telegram_user, created = await sync_to_async(
                    TelegramUser.objects.get_or_create
                )(
                    user=django_user,
                    defaults={"telegram_id": str(update.effective_chat.id)},
                )

                if created:
                    await update.message.reply_text(
                        "Вы успешно зарегистрированы в системе!"
                    )
                    logger.info(
                        f"Новый пользователь Telegram зарегистрирован: {phone} - {update.effective_chat.id}"
                    )
                else:
                    if telegram_user.telegram_id != str(update.effective_chat.id):
                        telegram_user.telegram_id = str(update.effective_chat.id)
                        await sync_to_async(telegram_user.save)()
                        await update.message.reply_text(
                            "Ваш Telegram ID успешно обновлен!"
                        )
                        logger.info(
                            f"Telegram ID пользователя обновлен: {phone} - {update.effective_chat.id}"
                        )
                    else:
                        await update.message.reply_text("Ваш Telegram ID уже актуален.")

            except Exception as e:
                await update.message.reply_text(
                    "Произошла ошибка при создании/обновлении Telegram ID."
                )
                logger.error(f"Telegram ID creation/update error: {e}", exc_info=True)

        else:
            await update.message.reply_text(
                "Пользователь с таким номером телефона не найден в системе."
            )

    except Exception as e:
        await update.message.reply_text(
            "Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз."
        )
        logger.error(f"Registration error: {e}", exc_info=True) 

    finally:
        db.close()



def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), receive_phone)
    )
    application.run_polling()
