from typing import Any, TypeVar, Type

import requests
from django.conf import settings
from pydantic import BaseModel

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

T = TypeVar('T', bound=BaseModel)


class TgClient:
    def __init__(self):
        self.token = settings.TGBOT_TOKEN
        self.default_url = settings.TELEGRAM_API_URL

    def _get_url(self, method: str) -> str:
        return f"{self.default_url}{self.token}/{method}"

    def _get_response(self, method: str, params: dict[str, Any], response_class: Type[T]) -> T:
        """
        Get response from Telegram API
        """
        response = requests.get(self._get_url(method), params=params)
        return response_class(**response.json())

    def get_updates(self, offset: int = 0, timeout: int = 10) -> T:
        """
        Get new messages from Telegram API
        """
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}

        return self._get_response(method, params, GetUpdatesResponse)

    def send_message(self, chat_id: int, text: str, timeout: int = 10) -> T:
        """
        Send message to tg_user using Telegram API
        """
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, 'timeout': timeout}

        return self._get_response(method, params, SendMessageResponse)
