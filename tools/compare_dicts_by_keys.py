from typing import Any
from random import choice


def compare_dicts_by_keys(
        dict_original: dict[str, Any],
        dict_expected: dict[str, Any],
        keys: list[str],
        exception_message: str
):
    """
        Сравнивает 2 словаря по выбранным ключам.

        Args:
            dict_original (dict): Словарь #1.
            dict_expected (dict): Словарь #2.
            keys (list[str]): Список ключей для сравнения.
            exception_message: Текст ошибки в случае расхождения данных.
        """
    dict_expected_filtered = {}
    for key in keys:
        dict_expected_filtered[key] = dict_expected.get(key)

    assert dict_original == dict_expected_filtered, exception_message