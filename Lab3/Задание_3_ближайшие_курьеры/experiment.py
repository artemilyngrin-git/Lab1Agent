import contextlib
import io
import logging
import random

import config
from agents_dispatcher import AgentsDispatcher
from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity
from scene import Scene
from stats import MessageStats

ORDER_TYPES = ['Документы', 'Посылки', 'Крупногабарит']
ORDERS_COUNT = 50
COURIERS_COUNT = 20
SEED = 42


def generate_data(seed=SEED):
    rnd = random.Random(seed)
    couriers = []
    for i in range(COURIERS_COUNT):
        couriers.append({
            'Табельный номер': 2000 + i,
            'ФИО': f'Курьер-{i + 1}',
            'Координата начала x': rnd.randint(0, 100),
            'Координата начала y': rnd.randint(0, 100),
            'Типы доставляемых заказов': ';'.join(rnd.sample(ORDER_TYPES, 2)),
            'Стоимость выхода на работу': rnd.randint(100, 300),
            'Цена работы за единицу времени': rnd.randint(2, 6),
            'Скорость': rnd.randint(4, 12),
            'Объем ранца': rnd.randint(15, 50),
            'Грузоподъемность': rnd.randint(30, 100),
        })
    orders = []
    for i in range(ORDERS_COUNT):
        time_from = rnd.randint(0, 100)
        orders.append({
            'Номер': i + 1,
            'Наименование': f'Заказ-{i + 1}',
            'Масса': rnd.randint(1, 30),
            'Объем': rnd.randint(1, 10),
            'Стоимость': rnd.randint(300, 3000),
            'Координата получения x': rnd.randint(0, 100),
            'Координата получения y': rnd.randint(0, 100),
            'Координата доставки x': rnd.randint(0, 100),
            'Координата доставки y': rnd.randint(0, 100),
            'Время получения заказа': time_from,
            'Время доставки заказа': time_from + 60,
            'Тип заказа': rnd.choice(ORDER_TYPES),
        })
    return couriers, orders


def run(nearest_count):
    config.NEAREST_COUNT = nearest_count
    MessageStats.reset()
    couriers_data, orders_data = generate_data()
    scene = Scene()
    dispatcher = AgentsDispatcher(scene)
    for row in couriers_data:
        dispatcher.add_entity(CourierEntity({}, row, scene))
    for row in orders_data:
        dispatcher.add_entity(OrderEntity({}, row, scene))
    couriers = scene.get_entities_by_type('COURIER')
    orders = scene.get_entities_by_type('ORDER')
    result = {
        'nearest': nearest_count or 'все',
        'messages': MessageStats.total(),
        'price_requests': MessageStats.counter['PRICE_REQUEST'],
        'planned': sum(1 for o in orders if o.courier is not None),
        'cost': sum(item.cost for c in couriers for item in c.schedule),
        'finish': max(c.get_last_time() for c in couriers),
    }
    dispatcher.actor_system.shutdown()
    return result


if __name__ == '__main__':
    logging.disable(logging.INFO)
    with contextlib.redirect_stdout(io.StringIO()):
        results = [run(count) for count in (None, 10, 5, 3)]
    print(f'{ORDERS_COUNT} заказов, {COURIERS_COUNT} курьеров')
    print(f'{"Опрашивать":>11} {"Сообщений":>10} {"Запросов цены":>14} {"Запланировано":>14} '
          f'{"Стоимость":>10} {"Конец работ":>12}')
    for r in results:
        print(f'{str(r["nearest"]):>11} {r["messages"]:>10} {r["price_requests"]:>14} '
              f'{r["planned"]:>14} {r["cost"]:>10.1f} {r["finish"]:>12.1f}')
