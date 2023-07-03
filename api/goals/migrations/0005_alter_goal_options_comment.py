# Generated by Django 4.2.2 on 2023-07-03 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0004_alter_goal_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Цель', 'verbose_name_plural': 'Цели'},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('goals', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Комментарии', to='goals.goal', verbose_name='Цель')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Комментарии', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
