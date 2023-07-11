from django.db import models

from core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлено", auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self):
        return self.title


class BoardParticipant(BaseModel):
    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name='role', choices=Role.choices, default=Role.owner)

    def __str__(self):
        return f'BoardParticipant {self.user}, {self.board}'


class Category(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Goal(BaseModel):
    class StatusChoices(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнена'
        archived = 4, 'В архиве'

    class PriorityChoices(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='goals')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goals')
    status = models.PositiveSmallIntegerField(verbose_name='Статус',
                                              choices=StatusChoices.choices,
                                              default=StatusChoices.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет',
                                                choices=PriorityChoices.choices,
                                                default=PriorityChoices.low)

    due_date = models.DateField(verbose_name='Дедлайн', null=True, blank=True)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title


class Comment(BaseModel):
    user = models.ForeignKey(User, verbose_name='Автор', related_name='comments', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment for {self.goal}'
