from entities.base_entity import BaseEntity
from entities.schedule_item import ScheduleItem
from point import Point
from utils.excel_utils import find_value, find_coordinate


class CourierEntity(BaseEntity):

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

    def supports_type(self, order_type) -> bool:

        return str(order_type).strip().lower() in self.types

    def add_order_to_schedule(self, order, time_from, time_to, price, params) -> bool:
        if time_from < self.get_last_time():
            return False
        item = ScheduleItem(order=order, rec_type='Доставка заказа',
                            start_time=time_from, end_time=time_to,
                            point_from=self.get_last_point(), point_to=order.point_to,
                            cost=price, all_params=params)
        self.schedule.append(item)
        order.courier = self
        return True

    def __repr__(self):
        return f'Курьер {self.name}'
