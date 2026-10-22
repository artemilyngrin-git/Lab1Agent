import logging

from agents_dispatcher import AgentsDispatcher
from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity
from scene import Scene
from stats import MessageStats
from utils.excel_utils import get_excel_data
from utils.output_utils import save_schedule, format_conflicts

DATA_FILE = 'Исходные данные.xlsx'
SCHEDULE_FILE = 'Расписание.txt'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

    scene = Scene()
    dispatcher = AgentsDispatcher(scene)

    for row in get_excel_data(DATA_FILE, 'Курьеры'):
        dispatcher.add_entity(CourierEntity({}, row, scene))

    for row in get_excel_data(DATA_FILE, 'Заказы'):
        dispatcher.add_entity(OrderEntity({}, row, scene))

    save_schedule(scene, SCHEDULE_FILE)
    print()
    print(format_conflicts(scene, 4.0, 12.0))
    print()
    print(f'Сообщений между агентами: {MessageStats.total()} {dict(MessageStats.counter)}')
    dispatcher.actor_system.shutdown()
