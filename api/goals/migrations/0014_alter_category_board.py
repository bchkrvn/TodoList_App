# Generated by Django 4.2.2 on 2023-07-10 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0013_create_new_objects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='goals.board', verbose_name='Доска'),
        ),
    ]
