from typing import Dict

import allure
import json


def compare_dicts_by_keys(
    dict_original: Dict,
    dict_expected: Dict,
    keys: list[str],
    exception_message: str,
    negative: bool = False,
    reason: str = None,
):
    """
    Сравнивает 2 словаря по выбранным ключам.

    Args:
        dict_original (dict): Словарь #1.
        dict_expected (dict): Словарь #2.
        keys (list[str]): Список ключей для сравнения.
        exception_message: Текст ошибки в случае расхождения данных.
        negative: True - Ожидается расхождение в данных; False - Ожидается сходство в данных.
        reason: Описание, зачем и при каких обстоятельствах мы сравниваем словари (для Allure)
    """
    dict_original_filtered = {}
    dict_expected_filtered = {}

    with allure.step(reason):
        allure.attach(
            json.dumps(dict_original, indent=4, ensure_ascii=False, default=str),
            name="Оригинальный словарь",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            json.dumps(dict_expected, indent=4, ensure_ascii=False, default=str),
            name="Словарь к сравнению",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            str(keys),
            name="Ключи, по которым сравниваем",
            attachment_type=allure.attachment_type.TEXT,
        )

        for key in keys:
            dict_original_filtered[key] = dict_original.get(key)
            dict_expected_filtered[key] = dict_expected.get(key)

        if negative:
            assert dict_original_filtered != dict_expected_filtered, (
                f"{exception_message}\n"
                f"EXPECTED: {dict_expected_filtered}\n"
                f"ACTUAL: {dict_original_filtered}"
            )
        else:
            assert dict_original_filtered == dict_expected_filtered, (
                f"{exception_message}\n"
                f"EXPECTED: {dict_expected_filtered}\n"
                f"ACTUAL: {dict_original_filtered}"
            )
