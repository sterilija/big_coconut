from datetime import datetime

def is_sorted_by_created_at(items, asc=True):
    """
    Проверяет, отсортирован ли список по createdAt.

    :param items: Список словарей типа Movie
    :param asc: True — по возрастанию, False — по убыванию
    :return: True/False
    """
    # преобразуем строки времени в datetime
    dates = [
        datetime.fromisoformat(item["createdAt"].replace("Z", "+00:00"))
        for item in items
    ]

    # проверяем порядок
    for i in range(len(dates) - 1):
        if asc:
            if dates[i] > dates[i + 1]:
                return False
        else:
            if dates[i] < dates[i + 1]:
                return False

    return True