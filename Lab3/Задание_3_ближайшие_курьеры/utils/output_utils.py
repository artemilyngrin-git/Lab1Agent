def format_schedule(scene):
    lines = []
    total_cost = 0.0
    for courier in scene.get_entities_by_type('COURIER'):
        lines.append(f'{courier.name} (таб. № {courier.number}), скорость {courier.velocity}, '
                     f'ставка {courier.rate}, старт {courier.start_point}')
        if not courier.schedule:
            lines.append('    расписание пусто')
        for item in courier.schedule:
            lines.append(f'    [{item.start_time:8.2f} - {item.end_time:8.2f}] {item.rec_type}: '
                         f'заказ {item.order.number} "{item.order.name}", '
                         f'{item.point_from} -> {item.point_to}, стоимость {item.cost:.2f}')
            total_cost += item.cost
        lines.append('')
    unplanned = [o for o in scene.get_entities_by_type('ORDER') if o.courier is None]
    if unplanned:
        lines.append('Не распределены заказы: ' + ', '.join(str(o.number) for o in unplanned))
    else:
        lines.append('Все заказы распределены')
    lines.append(f'Суммарная стоимость работы курьеров: {total_cost:.2f}')
    return '\n'.join(lines)


def save_schedule(scene, filename):
    text = format_schedule(scene)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(text)


def format_conflicts(scene, start_time, end_time):
    lines = [f'Записи расписания, пересекающиеся с интервалом [{start_time}; {end_time}]:']
    for courier in scene.get_entities_by_type('COURIER'):
        conflicts = courier.get_conflicts(start_time, end_time)
        lines.append(f'  {courier.name}: {len(conflicts)}')
        for item in conflicts:
            lines.append(f'    [{item.start_time:8.2f} - {item.end_time:8.2f}] {item.rec_type}, '
                         f'заказ {item.order.number}')
    return '\n'.join(lines)
