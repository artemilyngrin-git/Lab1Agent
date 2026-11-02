import logging

import config
from agent_base import AgentBase
from message import Message, MessageType


class OrderAgent(AgentBase):

    MAX_ATTEMPTS = 10

    def __init__(self):
        super().__init__()
        self.name = 'Агент заказа'
        self.possible_variants = []
        self.unchecked_couriers = []
        self.chosen_variant = None
        self.attempts = 0
        self.subscribe(MessageType.PRICE_RESPONSE, self.handle_price_response)
        self.subscribe(MessageType.PLANNING_RESPONSE, self.handle_planning_response)

    def handle_init_message(self, message, sender):
        super().handle_init_message(message, sender)
        self.__send_params_request()
    # step№1
    def __send_params_request(self):

        self.possible_variants = []
        self.unchecked_couriers = []
        all_couriers = self.scene.get_entities_by_type('COURIER')
        logging.info(f'{self} - список курьеров: {all_couriers}')
        for courier in all_couriers:
            if not courier.supports_type(self.entity.order_type):
                logging.info(f'{self} - типы грузов {courier} - {courier.types} '
                             f'не включают {self.entity.order_type}')
                continue
            courier_address = self.dispatcher.reference_book.get_address(courier)
            request_message = Message(MessageType.PRICE_REQUEST, self.entity)
            self.send(courier_address, request_message)
            self.unchecked_couriers.append(courier_address)
        if not self.unchecked_couriers:
            logging.warning(f'{self} - нет курьеров, возящих тип «{self.entity.order_type}»')

    def handle_price_response(self, message, sender):
        courier_variants = message.msg_body
        self.possible_variants.extend(courier_variants)
        self.unchecked_couriers.remove(sender)
        if not self.unchecked_couriers:
            self.__run_planning()
    # step№4
    def __evaluate_variants(self):

        if not self.possible_variants:
            return
        weights = config.get_weights()
        order = self.entity


        for variant in self.possible_variants:
            variant['window_violation'] = (max(0.0, order.time_from - variant['pickup_time'])
                                           + max(0.0, variant['time_to'] - order.time_to))

        all_pickups = [var.get('pickup_time') for var in self.possible_variants]
        min_pickup, max_pickup = min(all_pickups), max(all_pickups)
        all_finish_times = [var.get('time_to') for var in self.possible_variants]
        min_finish, max_finish = min(all_finish_times), max(all_finish_times)
        all_prices = [var.get('price') for var in self.possible_variants]
        min_price, max_price = min(all_prices), max(all_prices)
        all_violations = [var.get('window_violation') for var in self.possible_variants]
        min_violation, max_violation = min(all_violations), max(all_violations)

        for variant in self.possible_variants:

            start_efficiency = self.get_decreasing_kpi_value(
                variant.get('pickup_time'), min_pickup, max_pickup)
            finish_efficiency = self.get_decreasing_kpi_value(
                variant.get('time_to'), min_finish, max_finish)
            price_efficiency = self.get_decreasing_kpi_value(
                variant.get('price'), min_price, max_price)
            punctuality_efficiency = self.get_decreasing_kpi_value(
                variant.get('window_violation'), min_violation, max_violation)

            variant['start_efficiency'] = start_efficiency
            variant['finish_efficiency'] = finish_efficiency
            variant['price_efficiency'] = price_efficiency
            variant['punctuality_efficiency'] = punctuality_efficiency

            variant['total_efficiency'] = (weights['start'] * start_efficiency
                                           + weights['finish'] * finish_efficiency
                                           + weights['price'] * price_efficiency
                                           + weights['punctuality'] * punctuality_efficiency)

    def __run_planning(self):
        if not self.possible_variants:
            logging.warning(f'{self} - нет курьера, способного выполнить заказ')
            return
        self.__evaluate_variants()
        for variant in self.possible_variants:
            logging.info(f'{self} - вариант: {variant}')
        sorted_vars = sorted(self.possible_variants,
                             key=lambda v: (-round(v['total_efficiency'], 9),
                                            v['price'], v['time_to']))
        self.chosen_variant = sorted_vars[0]
        courier = self.chosen_variant['courier']
        logging.info(f'{self} - выбран {courier}, вариант {self.chosen_variant["variant_name"]}, '
                     f'оценка {self.chosen_variant["total_efficiency"]:.3f}, '
                     f'цена {self.chosen_variant["price"]:.2f}, '
                     f'завершение в {self.chosen_variant["time_to"]:.2f}')
        courier_address = self.dispatcher.reference_book.get_address(courier)
        self.send(courier_address, Message(MessageType.PLANNING_REQUEST, self.chosen_variant))

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
