from entities.base_entity import BaseEntity
from entities.order_entity import OrderEntity
from entities.schedule_item import ScheduleItem
from point import Point
from utils.excel_utils import find_value, find_coordinate


class CourierEntity(BaseEntity):
    """Класс курьера"""

    def __init__(self, onto_desc: {}, init_dict_data, scene=None):
        super().__init__(onto_desc, scene)
        self.number = find_value(init_dict_data, 'табель')
        self.name = find_value(init_dict_data, 'фио')
        x = float(find_coordinate(init_dict_data, 'x'))
        y = float(find_coordinate(init_dict_data, 'y'))
        self.start_point = Point(x, y)
        types_text = str(find_value(init_dict_data, 'тип'))
        self.types = [t.strip().lower() for t in types_text.split(';') if t.strip()]
        self.start_cost = float(find_value(init_dict_data, 'выход'))
        self.rate = float(find_value(init_dict_data, 'цен'))
        self.velocity = float(find_value(init_dict_data, 'скорост'))
        self.max_volume = float(find_value(init_dict_data, 'объем'))
        self.max_mass = float(find_value(init_dict_data, 'грузоподъем'))
        self.schedule = []
        self.uri = 'Courier' + str(self.number)

    def get_type(self):
        return 'COURIER'

    def get_last_point(self) -> Point:
        if not self.schedule:
            return self.start_point
        return self.schedule[-1].point_to

    def get_last_time(self) -> float:
        if not self.schedule:
            return 0.0
        return self.schedule[-1].end_time

    def can_carry(self, order: OrderEntity) -> bool:
        return (str(order.order_type).strip().lower() in self.types
                and order.weight <= self.max_mass
                and order.volume <= self.max_volume)

    def build_items(self, order: OrderEntity, start_time: float, params: dict):
        last_point = self.get_last_point()
        time_to_order = last_point.get_distance_to_other(order.point_from) / self.velocity
        arrive_time = start_time + time_to_order
        wait_time = max(0.0, order.time_from - arrive_time)
        carry_start = arrive_time + wait_time
        time_with_order = order.point_from.get_distance_to_other(order.point_to) / self.velocity
        carry_end = carry_start + time_with_order
        segments = [
            ('Движение за грузом', start_time, arrive_time, last_point, order.point_from),
            ('Ожидание', arrive_time, carry_start, order.point_from, order.point_from),
            ('Движение с грузом', carry_start, carry_end, order.point_from, order.point_to),
        ]
        return [ScheduleItem(order=order, rec_type=rec_type, start_time=start,
                             end_time=end, point_from=p_from, point_to=p_to,
                             cost=(end - start) * self.rate, all_params=params)
                for rec_type, start, end, p_from, p_to in segments]

    def add_order_to_schedule(self, order, time_from, time_to, price, params) -> bool:
        if time_from < self.get_last_time():
            return False
        items = self.build_items(order, time_from, params)
        self.schedule.extend(items)
        order.courier = self
        return True

    def __repr__(self):
        return f'Курьер {self.name}'
