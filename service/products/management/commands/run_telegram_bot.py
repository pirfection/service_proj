from django.core.management.base import BaseCommand
from products.session import Base, engine
from products import telegram_bot


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        telegram_bot.main()