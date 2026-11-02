import contextlib
import io
import logging

import config
from agents_dispatcher import AgentsDispatcher
from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity
from scene import Scene
from utils.excel_utils import get_excel_data
from utils.output_utils import count_in_window, total_cost

DATA_FILE = 'Исходные данные.xlsx'

# Три набора весов для таблицы в отчёте (сумма в каждом наборе = 1)
WEIGHT_SETS = {
    'А. Базовый (цена важнее всего)': {'start': 0.2, 'finish': 0.3, 'price': 0.5, 'punctuality': 0.0},
    'Б. Быстрее (сроки важнее цены)': {'start': 0.4, 'finish': 0.4, 'price': 0.1, 'punctuality': 0.1},
    'В. Точно в окно заказа': {'start': 0.05, 'finish': 0.05, 'price': 0.2, 'punctuality': 0.7},
}


def run(weights):
    config.set_weights(weights)
    scene = Scene()
    dispatcher = AgentsDispatcher(scene)
    for row in get_excel_data(DATA_FILE, 'Курьеры'):
        dispatcher.add_entity(CourierEntity({}, row, scene))
    for row in get_excel_data(DATA_FILE, 'Заказы'):
        dispatcher.add_entity(OrderEntity({}, row, scene))
    orders = scene.get_entities_by_type('ORDER')
    result = {
        'planned': sum(1 for o in orders if o.courier is not None),
        'total': len(orders),
        'cost': total_cost(scene),
        'in_window': count_in_window(scene),
        'variants': [item.all_params.get('variant_name')
                     for c in scene.get_entities_by_type('COURIER') for item in c.schedule],
    }
    dispatcher.actor_system.shutdown()
    return result


if __name__ == '__main__':
    logging.disable(logging.INFO)
    results = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for name, weights in WEIGHT_SETS.items():
            results[name] = run(weights)
    print(f'{"Набор весов":<34} {"Веса (start/finish/price/punct)":<34} {"Стоимость":>10} '
          f'{"Запланировано":>14} {"В окне":>7}  Варианты')
    for name, r in results.items():
        w = WEIGHT_SETS[name]
        weights_text = '/'.join(f'{w[k]:g}' for k in ('start', 'finish', 'price', 'punctuality'))
        print(f'{name:<34} {weights_text:<34} {r["cost"]:>10.2f} '
              f'{str(r["planned"]) + " из " + str(r["total"]):>14} {r["in_window"]:>7}  '
              f'{", ".join(r["variants"])}')
