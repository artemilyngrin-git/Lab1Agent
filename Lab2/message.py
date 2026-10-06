from enum import Enum
from dataclasses import dataclass
from typing import Any


class MessageType(Enum):
    INITIALIZATION = 'Инициализация'
    CREATE_ACTOR = 'Создание актора'
    HELLO_WORLD = 'Приветствие'


@dataclass
class Message:
    """Класс для хранения сообщений"""
    msg_type: MessageType
    msg_body: Any
