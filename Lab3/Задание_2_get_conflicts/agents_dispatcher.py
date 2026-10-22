import logging

from thespian.actors import ActorSystem

from courier_agent import CourierAgent
from entities.base_entity import BaseEntity
from log_config import LOG_CONFIG
from message import Message, MessageType
from order_agent import OrderAgent
from reference_book import ReferenceBook

TYPES_AGENTS = {
    'ORDER': OrderAgent,
    'COURIER': CourierAgent,
}


class AgentsDispatcher:
    """Класс диспетчера агентов"""

    def __init__(self, scene):
        self.actor_system = ActorSystem(logDefs=LOG_CONFIG)
        self.reference_book = ReferenceBook()
        self.scene = scene

    def add_entity(self, entity: BaseEntity):
        entity_type = entity.get_type()
        agent_type = TYPES_AGENTS.get(entity_type)
        if not agent_type:
            logging.warning(f'Для сущности типа {entity_type} не указан агент')
            return False
        self.scene.entities[entity_type].append(entity)
        self.create_agent(agent_type, entity)
        return True

    def create_agent(self, agent_class, entity):
        agent = self.actor_system.createActor(agent_class)
        self.reference_book.add_agent(entity=entity, agent_address=agent)
        init_data = {'dispatcher': self, 'scene': self.scene, 'entity': entity}
        init_message = Message(MessageType.INIT_MESSAGE, init_data)
        self.actor_system.tell(agent, init_message)
