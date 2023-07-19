from django.conf import settings
from django.core.management.base import BaseCommand
import secrets

from bot.tg.client import TgClient
from bot.models import TelegramUser
from bot.tg.dc import Update


class Command(BaseCommand):
    BOT_COMMANDS = ['/goals']
    TG_CLIENT = TgClient()

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.TG_CLIENT.get_updates(offset=offset)

            if res is None:
                continue

            for item in res.result:
                offset = item.update_id + 1

                # Если первое обращение
                if not TelegramUser.objects.filter(tg_user_id=item.message.from_.id,
                                                   tg_chat_id=item.message.chat.id).exists():
                    self.send_first_message(item)
                    continue

                # Если не авторизован
                if not TelegramUser.objects.filter(tg_user_id=item.message.from_.id,
                                                   tg_chat_id=item.message.chat.id).exclude(user=None).exists():
                    self.send_verification_code(item)
                    continue

                if item.message.text not in self.BOT_COMMANDS:
                    self.TG_CLIENT.send_message(item.message.chat.id, 'Неизвестная команда')

    def send_first_message(self, item: Update) -> None:
        message = 'Привет, новый пользователь!'
        TelegramUser.objects.create(tg_user_id=item.message.from_.id,
                                    tg_chat_id=item.message.chat.id)
        self.TG_CLIENT.send_message(item.message.chat.id, message)
        self.send_verification_code(item)

    def send_verification_code(self, item: Update):
        message = 'Для того, чтобы подключить приложение, введите на сайте следующий код:'
        token = secrets.token_hex(settings.TOKEN_LENGTH)
        TelegramUser.objects.filter(tg_user_id=item.message.from_.id,
                                    tg_chat_id=item.message.chat.id).update(verification_code=token)

        self.TG_CLIENT.send_message(item.message.chat.id, message)
        self.TG_CLIENT.send_message(item.message.chat.id, token)

    def send_goals(self, item):
        tg_user = TelegramUser.objects.get(tg_user_id=item.message.from_.id,
                                           tg_chat_id=item.message.chat.id)
        goals = tg_user.user.goals.all()

        if not goals:
            message = 'У вас нет целей'
        else:
            message = '*Ваши цели:* \n'
            for goal in goals:
                message += f'\n{goal.title}\n'
                if goal.due_date:
                    message += f'Дедлайн: {goal.due_date}\n'

        self.TG_CLIENT.send_message(item.message.chat.id, message)
