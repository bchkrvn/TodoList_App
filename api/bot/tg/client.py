import requests
import json
from django.conf import settings

from bot.tg import dc


class TgClient:
    def __init__(self):
        self.token = settings.TGBOT_TOKEN

    def _get_url(self, method: str) -> str:
        print(f"https://api.telegram.org/bot{self.token}/{method}")
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> dc.GetUpdatesResponse:
        method = 'getUpdates'
        params = {'timeout': timeout,
                  'offset': offset}

        response = requests.get(self._get_url(method), params=params)
        print(response.status_code)
        print(response.text)
        data = json.loads(response.text)

        updates = []
        for update in data['result']:
            message_data = update['message']
            updates.append(
                dc.Update(
                    update_id=update['update_id'],
                    message=dc.Message(
                        message_id=message_data['message_id'],
                        from_=dc.User(**message_data['from']),
                        chat=dc.Chat(**message_data['chat']),
                        date=message_data['date'],
                        text=message_data['text'],
                    )
                )
            )

            return dc.GetUpdatesResponse(ok=data['ok'], result=updates)

    def send_message(self, chat_id: int, text: str) -> dc.SendMessageResponse:
        method = 'sendMessage'
        params = {'chat_id': chat_id,
                  'text': text}
        response = requests.get(self._get_url(method), params=params)
        data = json.loads(response.text)
        print(data)
        return dc.SendMessageResponse(**data)
