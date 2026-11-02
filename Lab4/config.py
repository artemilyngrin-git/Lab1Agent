import logging

from utils.excel_utils import get_excel_data


CRITERIA_SHEET = 'Критерии'

CRITERIA = {
    'start': 'время получения заказа',
    'finish': 'время доставки заказа',
    'price': 'стоимость доставки',
    # смр2
    'punctuality': 'попадание во временное окно заказа',
}
# step№5
DEFAULT_WEIGHTS = {'start': 0.2, 'finish': 0.3, 'price': 0.5, 'punctuality': 0.0}

_weights = dict(DEFAULT_WEIGHTS)


def get_weights() -> dict:
    return dict(_weights)


def set_weights(weights: dict):

    unknown = set(weights) - set(CRITERIA)
    if unknown:
        raise ValueError(f'Неизвестные критерии: {sorted(unknown)}')
    new_weights = {key: float(weights.get(key, 0.0)) for key in CRITERIA}
    total = sum(new_weights.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f'Сумма весов должна быть равна 1, сейчас {total}')
    _weights.clear()
    _weights.update(new_weights)


def load_weights_from_excel(filename, sheet_name=CRITERIA_SHEET):

    try:
        rows = get_excel_data(filename, sheet_name)
    except ValueError:
        logging.warning(f'Лист «{sheet_name}» не найден, используются веса по умолчанию')
        set_weights(DEFAULT_WEIGHTS)
        return get_weights()
    set_weights({str(row['Критерий']).strip(): row['Вес'] for row in rows})
    logging.info(f'Веса критериев загружены из «{sheet_name}»: {get_weights()}')
    return get_weights()
