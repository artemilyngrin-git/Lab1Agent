from enum import Enum
from dataclasses import dataclass,field
from typing import Any
import time


class MessageType(Enum):
    INITIALIZATION = 'Инициализация'
    CREATE_ACTOR = 'Создание актора'
    HELLO_WORLD = 'Приветствие'
    SET_OPERATION = 'Выбор операции'

@dataclass
class Message:
    """Класс для хранения сообщений"""
    msg_type: MessageType
    msg_body: Any
    created_at: float = field(default_factory=time.perf_counter)
