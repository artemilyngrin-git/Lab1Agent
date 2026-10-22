from enum import Enum
from dataclasses import dataclass,field
from typing import Any
import time


class MessageType(Enum):
    INITIALIZATION = 'Инициализация'
    CREATE_ACTOR = 'Создание актора'
    HELLO_WORLD = 'Приветствие'
    SET_OPERATION = 'Выбор операции'
    REJECTED = 'Отказ'
    INIT_MESSAGE = 'Инициализация агента'
    PRICE_REQUEST = 'Запрос вариантов доставки'
    PRICE_RESPONSE = 'Варианты доставки'
    PLANNING_REQUEST = 'Запрос на планирование'
    PLANNING_RESPONSE = 'Результат планирования'

@dataclass
class Message:
    msg_type: MessageType
    msg_body: Any
    created_at: float = field(default_factory=time.perf_counter)
