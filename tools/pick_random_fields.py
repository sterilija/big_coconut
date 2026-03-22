import random

def pick_random_fields(data: dict) -> dict:
    keys = list(data.keys())
    k = random.randint(1, len(keys))  # сколько полей взять
    selected_keys = random.sample(keys, k)
    return {key: data[key] for key in selected_keys}