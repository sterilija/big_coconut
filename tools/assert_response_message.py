import allure
from typing import Literal

CHECK_IS_IN_MSG = "Проверяем, что ответ содержит ожидаемое сообщение внутри"
CHECK_IS_EQUAL_MSG = "Проверяем, что ответ полностью соответствует ожидаемому сообщению"


def _as_parts(message: str | list[str]) -> list[str]:
    if isinstance(message, list):
        return message
    return [message]


def _contains_message(expected: str | list[str], response: str | list[str]) -> bool:
    if isinstance(expected, list):
        return all(_contains_message(part, response) for part in expected)

    if isinstance(response, list):
        return any(expected in part for part in response)

    return expected in response


def _messages_equal(expected: str | list[str], response: str | list[str]) -> bool:
    if isinstance(expected, list) and isinstance(response, list):
        return sorted(expected) == sorted(response)
    return expected == response


def assert_response_message(
    reason: str,
    response_message: str | list[str],
    expected_message: str | list[str],
    assertion_message: str = "Пришедшее сообщение не соответствует ожидаемому",
    checking_type: Literal["equal", "in"] = "equal",
):
    def attach_messages():
        allure.attach(
            str(expected_message),
            name="Ожидаемое сообщение",
            attachment_type=allure.attachment_type.TEXT,
        )

        allure.attach(
            str(response_message),
            name="Пришедшее сообщение",
            attachment_type=allure.attachment_type.TEXT,
        )

        allure.attach(
            str(checking_type),
            name="Тип проверки",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(reason):
        if checking_type == "in":
            with allure.step(CHECK_IS_IN_MSG):
                attach_messages()
                assert _contains_message(expected_message, response_message), (
                    assertion_message
                )

        if checking_type == "equal":
            with allure.step(CHECK_IS_EQUAL_MSG):
                attach_messages()
                assert _messages_equal(expected_message, response_message), (
                    assertion_message
                )
