from django.db import models
from goals.models import Category
from core.models import User


class TelegramUser(models.Model):
    class Position(models.IntegerChoices):
        not_authorized = 1, "Не авторизован"
        wait_command = 2, 'Ожидание команды'
        choose_category = 3, "Выбор категории"
        create_goal = 4, "Создание цели"

    tg_chat_id = models.BigIntegerField()
    verification_code = models.CharField(max_length=30, null=True, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    position = models.PositiveIntegerField(choices=Position.choices, default=Position.not_authorized)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'TG_User {self.user}'if self.user else f'TG_User {self.tg_chat_id}'
