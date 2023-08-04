import requests
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from bot.models import TelegramUser
from bot.tg.dc import SendMessageResponse

User = get_user_model()


@shared_task
def send_message_task(url: str, params: dict) -> SendMessageResponse:
    response = requests.get(url, params=params)
    return SendMessageResponse(**response.json())


@shared_task
def change_bot_position_task(tg_user_id: int, position: int, category_id: int or None) -> TelegramUser:
    tg_user = TelegramUser.objects.get(id=tg_user_id)
    tg_user.position = position
    tg_user.category_id = category_id
    tg_user.save()
    return tg_user


@shared_task
def set_token_task(tg_user_id: int, token: str) -> TelegramUser:
    tg_user = TelegramUser.objects.get(id=tg_user_id)
    tg_user.verification_code = token
    tg_user.save()
    return tg_user


@shared_task
def send_email_task(user_id: int) -> SendMessageResponse:
    user = User.objects.get(id=user_id)
    subject = f'Подключение телеграм бота'
    message = f'{user.get_full_name()}, Вы успешно подключили телеграм бота.'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    return mail_sent
