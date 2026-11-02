import logging
import typing

from agent_base import AgentBase
from entities.order_entity import OrderEntity
from message import Message, MessageType
from point import Point

EPS = 1e-6

class CourierAgent(AgentBase):

    def __init__(self):
        super().__init__()
        self.name = 'Агент курьера'
        self.subscribe(MessageType.PRICE_REQUEST, self.handle_price_request)
        self.subscribe(MessageType.PLANNING_REQUEST, self.handle_planning_request)

    def handle_price_request(self, message, sender):
        order = message.msg_body
        variants = self.__get_params(order)
        if not variants:
            logging.info(f'{self} не может везти {order}')
        self.send(sender, Message(MessageType.PRICE_RESPONSE, variants))
    # step№2
    def __get_params(self, order: OrderEntity) -> typing.List:
        if order.weight > self.entity.max_mass:
            return []
        if order.volume > self.entity.max_volume:
            return []

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
        params = []

        # Вариант 1: asap - выезжаем сразу, как освободились (план «в хвост» расписания)
        asap_time_from = last_time
        params.append(self.__make_variant(order, 'asap', asap_time_from, time_to_order,
                                          duration, price))

        # Вариант 2: jit - заберём груз ровно в желаемое время получения
        # step№6
        jit_time_from = order.time_from - time_to_order
        if jit_time_from > asap_time_from + EPS:
            params.append(self.__make_variant(order, 'jit', jit_time_from, time_to_order,
                                              duration, price))

        # Вариант 3: jit_delivery - доставим ровно к желаемому времени доставки
        # смр 1
        jit_delivery_time_from = order.time_to - duration
        if (jit_delivery_time_from > asap_time_from + EPS
                and abs(jit_delivery_time_from - jit_time_from) > EPS):
            params.append(self.__make_variant(order, 'jit_delivery', jit_delivery_time_from,
                                              time_to_order, duration, price))
        return params

    def __make_variant(self, order, name, time_from, time_to_order, duration, price) -> dict:
        return {'courier': self.entity, 'time_from': time_from,
                'pickup_time': time_from + time_to_order,
                'time_to': time_from + duration, 'price': price,
                'order': order, 'variant_name': name}

    def handle_planning_request(self, message, sender):
        params = message.msg_body
        adding_result = self.entity.add_order_to_schedule(
            params.get('order'), params.get('time_from'),
            params.get('time_to'), params.get('price'), params)
        result_msg = Message(MessageType.PLANNING_RESPONSE, adding_result)
        self.send(sender, result_msg)
