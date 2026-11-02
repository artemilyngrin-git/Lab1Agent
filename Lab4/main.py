import logging

import config
from agents_dispatcher import AgentsDispatcher
from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity
from scene import Scene
from utils.excel_utils import get_excel_data
from utils.output_utils import save_schedule

DATA_FILE = 'Исходные данные.xlsx'
SCHEDULE_FILE = 'Расписание.txt'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

    # Критерии и веса читаются из листа «Критерии» файла с исходными данными
    config.load_weights_from_excel(DATA_FILE)

    scene = Scene()
    dispatcher = AgentsDispatcher(scene)

    for row in get_excel_data(DATA_FILE, 'Курьеры'):
        dispatcher.add_entity(CourierEntity({}, row, scene))

    for row in get_excel_data(DATA_FILE, 'Заказы'):
        dispatcher.add_entity(OrderEntity({}, row, scene))

    save_schedule(scene, SCHEDULE_FILE)
    dispatcher.actor_system.shutdown()
