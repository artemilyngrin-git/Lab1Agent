import logging
import typing

from agent_base import AgentBase
from entities.order_entity import OrderEntity
from message import Message, MessageType
from point import Point


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
        p1 = order.point_from
        last_point: Point = self.entity.get_last_point()
        distance_to_order = last_point.get_distance_to_other(p1)
        p2 = order.point_to
        distance_with_order = p1.get_distance_to_other(p2)
        time_to_order = distance_to_order / self.entity.velocity
        time_with_order = distance_with_order / self.entity.velocity
        duration = time_to_order + time_with_order
        price = duration * self.entity.rate

        last_time = self.entity.get_last_time()
        asap_time_from = last_time
        asap_time_to = asap_time_from + duration
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
