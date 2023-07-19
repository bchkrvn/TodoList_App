from django.db import models
from core.models import User


class TelegramUser(models.Model):
    class Position(models.IntegerChoices):
        not_authorized = 1, "Не авторизован"
        wait_command = 2, 'Ожидание команды'
        category_choose = 3, "Выбор категории"
        goal_creating = 4, "Создание цели"

    tg_chat_id = models.IntegerField()
    tg_user_id = models.IntegerField()
    verification_code = models.CharField(max_length=30, null=True, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    position = models.PositiveIntegerField(choices=Position.choices, default=Position.not_authorized)
