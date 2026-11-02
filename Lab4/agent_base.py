from abc import ABC
from typing import Dict, Callable, Any
import logging
import traceback
import time

from thespian.actors import Actor, ActorAddress

from message import MessageType, Message


class AgentBase(ABC, Actor):

    def __init__(self):
        super().__init__()
        self.name = 'Базовый агент'
        self.handlers: Dict[MessageType, Callable[[Any, ActorAddress], None]] = {}
        self.scene = None
        self.dispatcher = None
        self.entity = None
        self.subscribe(MessageType.HELLO_WORLD, self.handle_hello_world)
        self.subscribe(MessageType.INIT_MESSAGE, self.handle_init_message)

    def subscribe(self, msg_type: MessageType, handler: Callable[[Any, ActorAddress], None]):
        if msg_type in self.handlers:
            logging.warning('Повторная подписка на сообщение: %s', msg_type)
        self.handlers[msg_type] = handler
        
    def unsubscribe(self, msg_type: MessageType) -> bool:
        if msg_type not in self.handlers:
            logging.warning('%s: отписка от сообщения без подписки: %s', self.name, msg_type)
            return False
        del self.handlers[msg_type]
        return True

    def receiveMessage(self, msg, sender):
        logging.debug('%s получил сообщение: %s', self.name, msg)

        if isinstance(msg, Message):
            message_type = msg.msg_type
            if message_type in self.handlers:
                delay_ms = (time.perf_counter() - msg.created_at) * 1000
                print(f'{self.name}: задержка {delay_ms:.4f} мс ({message_type.value})')
                try:
                    self.handlers[message_type](msg, sender)
                except Exception as ex:
                    traceback.print_exc()
                    logging.error(ex)
            else:
                logging.warning('%s Отсутствует подписка на сообщение: %s',
                                self.name, message_type)

    def handle_hello_world(self, message, sender):
        print("Hello, world")

    def handle_init_message(self, message, sender):
        message_data = message.msg_body
        self.scene = message_data.get('scene')
        self.dispatcher = message_data.get('dispatcher')
        self.entity = message_data.get('entity')
        self.name = self.name + ' ' + self.entity.name
        logging.info(f'{self} проинициализирован')


        # step№3
    @staticmethod
    def get_decreasing_kpi_value(value: float, min_value: float, max_value: float):

        if max_value == min_value:
            return 1
        if value > max_value or value < min_value:
            return -1
        if isinstance(value, float) and abs(value - min_value) < 0.000001:
            return 1
        if isinstance(value, float) and abs(value - max_value) < 0.000001:
            return 0
        return 1 - (value - min_value) / (max_value - min_value)

    @staticmethod
    def get_increasing_kpi_value(value: float, min_value: float, max_value: float):
        if max_value == min_value:
            return 1
        if value > max_value or value < min_value:
            return -1
        if isinstance(value, float) and abs(value - min_value) < 0.000001:
            return 0
        if isinstance(value, float) and abs(value - max_value) < 0.000001:
            return 1
        return (value - min_value) / (max_value - min_value)

    def __str__(self):
        return self.name
