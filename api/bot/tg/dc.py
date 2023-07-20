from dataclasses import dataclass
from typing import List


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    from_: User
    chat: Chat
    date: int
    text: str


@dataclass
class Update:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Update]


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message
