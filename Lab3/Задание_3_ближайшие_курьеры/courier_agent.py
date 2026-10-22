import logging
import typing

from agent_base import AgentBase
from entities.order_entity import OrderEntity
from message import Message, MessageType


class CourierAgent(AgentBase):
    """Агент курьера: оценивает условия доставки и ведёт расписание"""

    def __init__(self):
        super().__init__()
        self.name = 'Агент курьера'
        self.subscribe(MessageType.PRICE_REQUEST, self.handle_price_request)
        self.subscribe(MessageType.PLANNING_REQUEST, self.handle_planning_request)

    def handle_price_request(self, message, sender):
        order = message.msg_body
        if self.entity.can_carry(order):
            variants = self.__get_params(order)
        else:
            variants = []
            logging.info(f'{self} не может везти {order}')
        self.send(sender, Message(MessageType.PRICE_RESPONSE, variants))

    def __get_params(self, order: OrderEntity) -> typing.List:
        """Формирует возможные варианты размещения заказа"""
        last_time = self.entity.get_last_time()
        items = self.entity.build_items(order, last_time, {})
        asap_time_from = items[0].start_time
        asap_time_to = items[-1].end_time
        price = sum(item.cost for item in items)
        asap_variant = {'courier': self.entity, 'time_from': asap_time_from,
                        'time_to': asap_time_to, 'price': price,
                        'order': order, 'variant_name': 'asap'}
        return [asap_variant]

    def handle_planning_request(self, message, sender):
        params = message.msg_body
        adding_result = self.entity.add_order_to_schedule(
            params.get('order'), params.get('time_from'),
            params.get('time_to'), params.get('price'), params)
        result_msg = Message(MessageType.PLANNING_RESPONSE, adding_result)
        self.send(sender, result_msg)
