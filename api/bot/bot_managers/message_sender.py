from django.conf import settings
import secrets
from django.db.models import QuerySet

from bot.tg.client import TgClient
from goals.models import Category, Goal


class MessageSender:
    tg_client = TgClient()

    def _send_message(self, chat: id, message: str) -> None:
        self.tg_client.create_and_send_message(chat, message)

    def send_new_user_message(self, chat: int) -> None:
        """
        Send a message to a new user in the bot
        """
        message = 'Привет, новый пользователь!'
        self._send_message(chat, message)

    def send_cancel_message(self, chat: int) -> None:
        """
        Send a message about successful cancel when user canceled the operation
        """
        message = 'Операция отменена'
        self._send_message(chat, message)

    def send_goal_create_error_message(self, chat: int) -> None:
        """
        Send a message about bad category selection
        """
        message = 'Введите верный id категории'
        self._send_message(chat, message)

    def send_create_goal_message(self, chat: int, category: Category) -> None:
        """
        Send a message with a suggestion to choose a name for the goal
        """
        message = f'Введите новую цель для категории "{category.title}":' \
                  f'\nДля отмены введите /cancel'
        self._send_message(chat, message)

    def send_goal_created_message(self, chat: int, goal: Goal) -> None:
        """
        Send a message about successful goal creating
        """
        message = f'Новая цель "{goal.title}" создана!'
        self._send_message(chat, message)

    def send_verification_code_and_get_token(self, chat: int) -> str:
        """
        Send a message with a verification code and return this verification code
        """
        message = 'Для того, чтобы подключить приложение, введите на сайте следующий код:\n'
        token = secrets.token_hex(settings.TOKEN_LENGTH)
        self._send_message(chat, message + token)
        # self._send_message(chat, token)
        return token

    def send_wrong_command_message(self, chat: int, commands: dict) -> None:
        """
        Send a message about invalid command
        """
        message = 'Неизвестная команда'
        message += '\nДоступные команды:\n' + '\n'.join(commands)
        self._send_message(chat, message)

    def send_goals_message(self, chat: int, goals: QuerySet) -> None:
        """
        Send a message with user's goals
        """
        if not goals:
            message = 'У вас нет целей'
        else:
            message = 'Ваши цели: \n'
            for goal in goals:
                message += f'\n{goal.title}\n'
                if goal.due_date:
                    message += f'Дедлайн: {goal.due_date.strftime("%d.%m.%Y")}\n'
        message += '\nДля создания новой цели отправьте команду /create'
        self._send_message(chat, message)

    def send_categories_message(self, chat: int, categories: QuerySet) -> None:
        """
        Send a message with user's categories where he isn't reader
        """
        if not categories:
            message = 'У вас нет доступных для создания целей категорий'
        else:
            message = 'Ваши категории, к которым можно создать цели: \n'
            for category in categories:
                message += f'\n{category.pk} - {category.title}\n'

            message += '\nДля выбора категории отправьте ее номер' \
                       '\nДля отмены введите /cancel'
        self._send_message(chat, message)
