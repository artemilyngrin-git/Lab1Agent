import logging

import config
from agent_base import AgentBase
from message import Message, MessageType


class OrderAgent(AgentBase):
    """Агент заказа: ищет курьера, который выполнит заказ"""

    MAX_ATTEMPTS = 10

    def __init__(self):
        super().__init__()
        self.name = 'Агент заказа'
        self.possible_variants = []
        self.unchecked_couriers = []
        self.asked_couriers = []
        self.chosen_variant = None
        self.attempts = 0
        self.subscribe(MessageType.PRICE_RESPONSE, self.handle_price_response)
        self.subscribe(MessageType.PLANNING_RESPONSE, self.handle_planning_response)

    def handle_init_message(self, message, sender):
        super().handle_init_message(message, sender)
        self.__send_params_request()

    def __send_params_request(self):
        self.possible_variants = []
        self.unchecked_couriers = []
        all_couriers = self.scene.get_entities_by_type('COURIER')
        if config.NEAREST_COUNT:
            couriers = self.scene.get_nearest_couriers(self.entity.point_from, config.NEAREST_COUNT)
        else:
            couriers = all_couriers
        self.asked_couriers = list(couriers)
        logging.info(f'{self} - опрашиваемые курьеры: {couriers}')
        self.__ask_couriers(couriers)

    def __ask_couriers(self, couriers):
        for courier in couriers:
            courier_address = self.dispatcher.reference_book.get_address(courier)
            request_message = Message(MessageType.PRICE_REQUEST, self.entity)
            self.send(courier_address, request_message)
            self.unchecked_couriers.append(courier_address)

    def handle_price_response(self, message, sender):
        courier_variants = message.msg_body
        self.possible_variants.extend(courier_variants)
        self.unchecked_couriers.remove(sender)
        if not self.unchecked_couriers:
            self.__run_planning()

    def __run_planning(self):
        if not self.possible_variants:
            self.__ask_remaining_couriers()
            return
        self.chosen_variant = min(self.possible_variants,
                                  key=lambda v: (v['price'], v['time_to']))
        courier = self.chosen_variant['courier']
        logging.info(f'{self} - выбран {courier}, цена {self.chosen_variant["price"]:.2f}, '
                     f'завершение в {self.chosen_variant["time_to"]:.2f}')
        courier_address = self.dispatcher.reference_book.get_address(courier)
        self.send(courier_address, Message(MessageType.PLANNING_REQUEST, self.chosen_variant))

    def __ask_remaining_couriers(self):
        all_couriers = self.scene.get_entities_by_type('COURIER')
        remaining = [c for c in all_couriers if c not in self.asked_couriers]
        if not remaining:
            logging.warning(f'{self} - нет курьера, способного выполнить заказ')
            return
        logging.info(f'{self} - ближайшие не подошли, опрашиваю остальных: {remaining}')
        self.asked_couriers.extend(remaining)
        self.__ask_couriers(remaining)

    def handle_planning_response(self, message, sender):
        if message.msg_body:
            logging.info(f'{self} - заказ запланирован у {self.chosen_variant["courier"]}')
            return
        logging.warning(f'{self} - отказ: вариант уже невыполним, повторяю переговоры')
        self.attempts += 1
        if self.attempts >= self.MAX_ATTEMPTS:
            logging.error(f'{self} - исчерпано число попыток')
            return
        self.__send_params_request()
