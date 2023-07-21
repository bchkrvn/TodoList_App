from django.core.management.base import BaseCommand

from bot.tg.client import TgClient
from bot.models import TelegramUser
from bot.tg.dc import Update
from .message_sender import MessageSender
from .db_manager import DBManager
from goals.models import Category


class Command(BaseCommand):
    tg_client = TgClient()
    tg_user = None
    cancel_word = '/cancel'
    message_sender = MessageSender()
    db_manager = DBManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            '/goals': self.send_goals,
            '/create': self.send_categories,
        }
        self.positions = {
            TelegramUser.Position.not_authorized: self.send_verification_code,
            TelegramUser.Position.wait_command: self.choose_command,
            TelegramUser.Position.choose_category: self.choose_category,
            TelegramUser.Position.create_goal: self.create_goal,
        }

    def handle(self, *args, **options) -> None:
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            if res is None:
                continue
            for item in res.result:
                offset = item.update_id + 1
                try:
                    self.tg_user = self.db_manager.get_tg_user(item.message.from_.id, item.message.chat.id)
                except TelegramUser.DoesNotExist:
                    self.tg_user = None
                    self.send_first_message(item)
                    continue
                self.choose_position(item)

    def send_first_message(self, item: Update) -> None:
        self.tg_user = self.db_manager.create_tg_user(item.message.from_.id, item.message.chat.id)
        self.message_sender.send_new_user_message(self.tg_user.tg_chat_id)
        self.send_verification_code(item)

    def choose_position(self, item: Update) -> None:
        """
        Choose user position in bot
        """
        self.positions[self.tg_user.position](item)

    def send_verification_code(self, item: Update) -> None:
        token = self.message_sender.send_verification_code_and_get_token(self.tg_user.tg_chat_id)
        self.db_manager.set_token_for_tg_user(self.tg_user, token)

    def choose_command(self, item: Update) -> None:
        if item.message.text in self.commands:
            self.commands[item.message.text](item)
        else:
            self.message_sender.send_wrong_command_message(self.tg_user.tg_chat_id, self.commands)

    def send_goals(self, item: Update) -> None:
        goals = self.db_manager.get_users_goals(self.tg_user)
        self.message_sender.send_goals_message(self.tg_user.tg_chat_id, goals)

    def send_categories(self, item: Update) -> None:
        categories = self.db_manager.get_users_categories(self.tg_user)
        self.message_sender.send_categories_message(self.tg_user.tg_chat_id, categories)
        self.tg_user.position = TelegramUser.Position.choose_category
        self.tg_user.save()

    def cancel(self) -> None:
        self.message_sender.send_cancel_message(self.tg_user.tg_chat_id)
        self.db_manager.change_position(self.tg_user, TelegramUser.Position.wait_command)

    def choose_category(self, item: Update) -> None:
        if item.message.text == self.cancel_word:
            self.cancel()
            return None

        try:
            category = self.db_manager.get_users_category(self.tg_user, item.message.text)
        except (Category.DoesNotExist, ValueError):
            self.message_sender.send_goal_create_error_message(self.tg_user.tg_chat_id)
            return None

        self.db_manager.change_position(self.tg_user, TelegramUser.Position.create_goal, category)
        self.message_sender.send_create_goal_message(self.tg_user.tg_chat_id, category)

    def create_goal(self, item: Update) -> None:
        if item.message.text == self.cancel_word:
            self.cancel()
            return None

        new_goal = self.db_manager.create_new_goal(category=self.tg_user.category,
                                                   title=item.message.text,
                                                   user=self.tg_user.user)
        self.db_manager.change_position(self.tg_user, TelegramUser.Position.wait_command)
        self.message_sender.send_goal_created_message(self.tg_user.tg_chat_id, new_goal)
