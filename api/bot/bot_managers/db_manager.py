from django.db.models import QuerySet

from goals.models import Goal, Category, BoardParticipant
from core.models import User
from bot.models import TelegramUser


class DBManager:

    def get_tg_user(self, user_id: int, chat_id: int) -> TelegramUser:
        return TelegramUser.objects.get(tg_user_id=user_id, tg_chat_id=chat_id)

    def create_tg_user(self, user_id: int, chat_id: int) -> TelegramUser:
        return TelegramUser.objects.create(tg_user_id=user_id, tg_chat_id=chat_id)

    def set_token_for_tg_user(self, tg_user: TelegramUser, token: str) -> None:
        tg_user.verification_code = token
        tg_user.save()

    def get_users_goals(self, tg_user: TelegramUser) -> QuerySet:
        return tg_user.user.goals.exclude(status=Goal.StatusChoices.archived)

    def get_users_categories(self, tg_user: TelegramUser) -> QuerySet:
        boards = [p.board for p in tg_user.user.participants.exclude(role=BoardParticipant.Role.reader,
                                                                     board__is_deleted=True)]
        return Category.objects.filter(board__in=boards, is_deleted=False).order_by('pk')

    def get_users_category(self, tg_user: TelegramUser, category_id: str) -> Category:
        users_categories = self.get_users_categories(tg_user)
        return users_categories.get(id=category_id)

    def change_position(self, tg_user: TelegramUser, position: int, category=None) -> None:
        tg_user.position = position
        tg_user.category = category
        tg_user.save()

    def create_new_goal(self, category: Category, title: str, user: User) -> Goal:
        return Goal.objects.create(category=category, title=title, user=user)
