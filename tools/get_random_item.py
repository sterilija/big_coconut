import random


def get_random_item(arr: list):
    if not arr:
        raise ValueError("Массив пуст")
    return random.choice(arr)