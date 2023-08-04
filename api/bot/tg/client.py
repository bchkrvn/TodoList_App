import requests
from django.conf import settings

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from .tasks import send_message_task


class TgClient:
    def __init__(self):
        self.token = settings.TGBOT_TOKEN
        self.default_url = settings.TELEGRAM_API_URL

    def _get_url(self, method: str) -> str:
        return f"{self.default_url}{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 10) -> GetUpdatesResponse:
        """
        Get new messages from Telegram API
        """
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self._get_url(method), params=params)
        return GetUpdatesResponse(**response.json())

    def create_and_send_message(self, chat_id: int, text: str, timeout: int = 10) -> SendMessageResponse:
        """
        Create and send message to tg_user using Telegram API
        """
        method = 'sendMessage'
        url = self._get_url(method)
        params = {'chat_id': chat_id, 'text': text, 'timeout': timeout}
        return send_message_task.delay(url, params)
