from django.conf import settings
from django.core.management.base import BaseCommand
import secrets
from django.db.models import QuerySet

from bot.tg.client import TgClient
from bot.models import TelegramUser
from bot.tg.dc import Update
from goals.models import Category, BoardParticipant, Goal


class Command(BaseCommand):
    tg_client = TgClient()
    tg_user = None
    cancel_word = '/cancel'

    def handle(self, *args, **options) -> None:
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)

            if res is None:
                continue

            for item in res.result:
                offset = item.update_id + 1
                try:
                    self.tg_user = TelegramUser.objects.get(tg_user_id=item.message.from_.id,
                                                            tg_chat_id=item.message.chat.id)
                except TelegramUser.DoesNotExist:
                    self.tg_user = None
                    self.send_first_message(item)
                    continue

                self.choose_position(item)

    def send_first_message(self, item: Update) -> None:
        message = 'Привет, новый пользователь!'
        self.tg_user = TelegramUser.objects.create(tg_user_id=item.message.from_.id,
                                                   tg_chat_id=item.message.chat.id)
        self.tg_client.send_message(item.message.chat.id, message)
        self.send_verification_code(item)

    def choose_position(self, item: Update) -> None:
        """
        Choose user position in bot
        """
        positions = {
            TelegramUser.Position.not_authorized: self.send_verification_code,
            TelegramUser.Position.wait_command: self.choose_command,
            TelegramUser.Position.choose_category: self.choose_category,
            TelegramUser.Position.create_goal: self.create_goal,
        }

        if item.message.text == self.cancel_word:
            self.cancel()
        else:
            positions[self.tg_user.position](item)

    def send_verification_code(self, item: Update) -> None:
        message = 'Для того, чтобы подключить приложение, введите на сайте следующий код:'
        token = secrets.token_hex(settings.TOKEN_LENGTH)
        self.tg_user.verification_code = token
        self.tg_user.save()

        self.tg_client.send_message(item.message.chat.id, message)
        self.tg_client.send_message(item.message.chat.id, token)

    def choose_command(self, item: Update) -> None:
        commands = {
            '/goals': self.send_goals,
            '/create': self.send_categories,
        }

        if item.message.text in commands:
            commands[item.message.text](item)
        else:
            message = 'Неизвестная команда'
            message += '\nДоступные команды:\n' + '\n'.join(commands.keys())
            self.tg_client.send_message(item.message.chat.id, message)

    def send_goals(self, item: Update) -> None:
        goals = self.tg_user.user.goals.exclude(status=Goal.StatusChoices.archived).all()

        if not goals:
            message = 'У вас нет целей'
        else:
            message = 'Ваши цели: \n'
            for goal in goals:
                message += f'\n{goal.title}\n'
                if goal.due_date:
                    message += f'Дедлайн: {goal.due_date}\n'
        message += '\nДля создания новой цели отправьте команду /create'
        self.tg_client.send_message(item.message.chat.id, message)

    def send_categories(self, item: Update) -> None:
        categories = self.get_users_categories()

        if not categories:
            message = 'У вас нет доступных для создания целей категорий'
        else:
            message = 'Ваши категории: \n'
            for category in categories:
                message += f'\n{category.pk} - {category.title}\n'

            message += '\nДля выбора категории отправьте ее номер' \
                       '\nДля отмены введите /cancel'

        self.tg_client.send_message(self.tg_user.tg_chat_id, message)
        self.tg_user.position = TelegramUser.Position.choose_category
        self.tg_user.save()

    def get_users_categories(self) -> QuerySet:
        user_boards = [p.board for p in self.tg_user.user.participants.exclude(role=BoardParticipant.Role.reader,
                                                                               board__is_deleted=True)]
        return Category.objects.filter(board__in=user_boards, is_deleted=False).order_by('pk')

    def cancel(self):
        message = 'Операция отменена'
        self.tg_client.send_message(self.tg_user.tg_chat_id, message)
        self.tg_user.position = TelegramUser.Position.wait_command
        self.tg_user.save()

    def choose_category(self, item: Update):
        try:
            category = self.get_users_categories().get(id=item.message.text)
        except (Category.DoesNotExist, ValueError):
            message = 'Введите верный id категории'
            self.tg_client.send_message(self.tg_user.tg_chat_id, message)
            return None

        self.tg_user.category = category
        self.tg_user.position = TelegramUser.Position.create_goal
        self.tg_user.save()

        message = f'Введите новую цель для категории "{category.title}":' \
                  f'\nДля отмены введите /cancel'
        self.tg_client.send_message(self.tg_user.tg_chat_id, message)

    def create_goal(self, item: Update) -> None:
        new_goal = Goal.objects.create(category=self.tg_user.category,
                                       title=item.message.text,
                                       user=self.tg_user.user)

        self.tg_user.position = TelegramUser.Position.wait_command
        self.tg_user.category = None
        self.tg_user.save()

        message = f'Новая цель "{new_goal.title} создана!"'
        self.tg_client.send_message(self.tg_user.tg_chat_id, message)
