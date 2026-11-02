EPS = 1e-6


def count_in_window(scene):
    count = 0
    for courier in scene.get_entities_by_type('COURIER'):
        for item in courier.schedule:
            pickup = item.all_params.get('pickup_time', item.start_time)
            if (pickup >= item.order.time_from - EPS
                    and item.end_time <= item.order.time_to + EPS):
                count += 1
    return count


def total_cost(scene):
    return sum(item.cost for c in scene.get_entities_by_type('COURIER') for item in c.schedule)


def format_schedule(scene):
    lines = []
    for courier in scene.get_entities_by_type('COURIER'):
        lines.append(f'{courier.name} (таб. № {courier.number}), скорость {courier.velocity}, '
                     f'ставка {courier.rate}, старт {courier.start_point}')
        if not courier.schedule:
            lines.append('    расписание пусто')
        for item in courier.schedule:
            variant = item.all_params.get('variant_name', '-')
            lines.append(f'    [{item.start_time:8.2f} - {item.end_time:8.2f}] {item.rec_type}: '
                         f'заказ {item.order.number} "{item.order.name}" '
                         f'(окно {item.order.time_from:g}-{item.order.time_to:g}, '
                         f'вариант {variant}), '
                         f'{item.point_from} -> {item.point_to}, стоимость {item.cost:.2f}')
        lines.append('')
    orders = scene.get_entities_by_type('ORDER')
    unplanned = [o for o in orders if o.courier is None]
    if unplanned:
        lines.append('Не распределены заказы: ' + ', '.join(str(o.number) for o in unplanned))
    else:
        lines.append('Все заказы распределены')
    lines.append(f'Суммарная стоимость работы курьеров: {total_cost(scene):.2f}')
    lines.append(f'Заказов в пределах своего временного окна: {count_in_window(scene)} '
                 f'из {len(orders) - len(unplanned)}')
    return '\n'.join(lines)


def save_schedule(scene, filename):
    text = format_schedule(scene)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(text)
