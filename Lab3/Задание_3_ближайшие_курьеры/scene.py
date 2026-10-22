from collections import defaultdict
import typing


class Scene:
    """Класс сцены для хранения сущностей виртуального мира"""

    def __init__(self):
        self.entities = defaultdict(list)

    def get_entities_by_type(self, entity_type) -> typing.List:
        return self.entities.get(entity_type, [])

    def get_nearest_couriers(self, point, count) -> typing.List:
        couriers = self.get_entities_by_type('COURIER')
        ranked = sorted(couriers, key=lambda c: c.get_last_point().get_distance_to_other(point))
        return ranked[:count]
