from collections import defaultdict
import typing


class Scene:
    """Класс сцены для хранения сущностей виртуального мира"""

    def __init__(self):
        self.entities = defaultdict(list)

    def get_entities_by_type(self, entity_type) -> typing.List:
        return self.entities.get(entity_type, [])
