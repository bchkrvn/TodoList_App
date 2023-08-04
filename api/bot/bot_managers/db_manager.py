from django.db.models import QuerySet

from goals.models import Goal, Category, BoardParticipant
from core.models import User
from bot.models import TelegramUser
from bot.tg.tasks import change_bot_position_task, set_token_task


class DBManager:

    def get_tg_user(self, chat_id: int) -> TelegramUser:
        """
        Get telegram user from DB
        """
        return TelegramUser.objects.get_or_create(tg_chat_id=chat_id)

    def set_token_for_tg_user(self, tg_user: TelegramUser, token: str) -> None:
        """
        Save user's token for authentication on the web-site in the DB
        """
        set_token_task.delay(tg_user_id=tg_user.pk, token=token)

    def get_users_goals(self, tg_user: TelegramUser) -> QuerySet:
        """
        Get all goals from all user's boards
        """
        users_goals = Goal.objects.filter(category__board__participants__user=tg_user.user).exclude(
            status=Goal.StatusChoices.archived)
        return users_goals

    def get_users_categories(self, tg_user: TelegramUser) -> QuerySet:
        """
        Get all categories in boards where user is not reader
        """
        boards = [p.board for p in tg_user.user.participants.exclude(role=BoardParticipant.Role.reader,
                                                                     board__is_deleted=True)]
        return Category.objects.filter(board__in=boards, is_deleted=False).order_by('pk')

    def get_users_category(self, tg_user: TelegramUser, category_id: str) -> Category:
        """
        Get category from all user's categories in boards where user is not reader
        """
        users_categories = self.get_users_categories(tg_user)
        return users_categories.get(id=category_id)

    def change_position(self, tg_user: TelegramUser, position: int, category=None) -> None:
        """
        Change tg bot position after user's request
        """
        change_bot_position_task.delay(tg_user_id=tg_user.pk, position=position,
                                       category_id=category.id if category else None)

    def create_new_goal(self, category: Category, title: str, user: User) -> Goal:
        """
        Create goal for selected user's category
        """
        return Goal.objects.create(category=category, title=title, user=user)
