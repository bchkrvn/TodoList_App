from django.db import models

from core.models import User


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлено", auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


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


class Goal(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='goals')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goals')
    status = models.PositiveSmallIntegerField(verbose_name='Статус',
                                              choices=StatusChoices.choices,
                                              default=StatusChoices.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет',
                                                choices=PriorityChoices.choices,
                                                default=PriorityChoices.low)

    due_date = models.DateField(verbose_name='Дедлайн', null=True, blank=True)
    created = models.DateTimeField(verbose_name='Создана', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='Автор', related_name='Комментарии',
                             on_delete=models.SET_NULL, null=True)
    goal = models.ForeignKey(Goal, verbose_name='Цель', related_name='Комментарии', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment for {self.goal}'
