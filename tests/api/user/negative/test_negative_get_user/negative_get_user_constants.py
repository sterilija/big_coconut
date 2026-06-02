from http import HTTPStatus

from faker import Faker

from constants.error_messages import ServerErrorMessages
from tests.testconstants import TestInitials, TestParameters
from tools.data_generator import DataGenerator

allure_file_description = """
    Тестирование негативных сценариев получения пользователя.
    Тесты, присутствующе в этом файле:
    1. (парам.) test_get_users_list_wrong_query - получение списка пользователей с неправильным query параметром
    2. (парам.) test_get_user_wrong_locator - получение пользователя по неправильному локатору
    3. (парам.) test_get_user_wrong_session_role - получение пользователя из-под неверной ролёвки
    """

fake = Faker()

STP_ERROR_COMPARISON_MSG = "Проверяем что ругань в ответе соответствует ожидаемой"


class TestsList:
    get_users_list_wrong_query = TestInitials(
        title="получение списка пользователей с неправ.query параметром, [{param_id}]",
        parameters=TestParameters(
            arg_names="query, expected_message, assertion_message, expected_status",
            arg_values=[
                (
                    {"pageSize": 0, "page": 1},
                    ServerErrorMessages.field_has_minimum_amount("pageSize", 1),
                    "Неверное сообщение в ответе при попытке получить список пользователей с pageSize < 1",
                    HTTPStatus.BAD_REQUEST,
                ),
                (
                    {"pageSize": 1, "page": 0},
                    ServerErrorMessages.field_has_minimum_amount("page", 1),
                    "Неверное сообщение в ответе при попытке получить список пользователей с page < 1",
                    HTTPStatus.BAD_REQUEST,
                ),
                (
                    {
                        "pageSize": fake.random_int(min=21),
                        "page": fake.random_int(min=1, max=30),
                    },
                    ServerErrorMessages.field_has_maximum_amount("pageSize", 20),
                    "Неверное сообщение в ответе при попытке получить список пользователей с pageSize > 20",
                    HTTPStatus.BAD_REQUEST,
                ),
                (
                    {"createdAt": fake.word()},
                    ServerErrorMessages.INTERNAL_ERROR,
                    "Неверное сообщение в ответе при попытке получить список пользователей с неверным значением createdAt",
                    HTTPStatus.INTERNAL_SERVER_ERROR,  # TODO BUG: 500 вместо 400 при неправильном query createdAt
                ),
                (
                    {"roles": fake.word()},
                    ServerErrorMessages.INTERNAL_ERROR,
                    "Неверное сообщение в ответе при попытке получить список пользователей с неверным форматом roles",
                    HTTPStatus.INTERNAL_SERVER_ERROR,  # TODO BUG: 500 вместо 400 при неправильном формате query roles
                ),
                (
                    {"roles": [fake.word()]},
                    ServerErrorMessages.INTERNAL_ERROR,
                    "Неверное сообщение в ответе при попытке получить список пользователей с неверным значением roles",
                    HTTPStatus.INTERNAL_SERVER_ERROR,  # TODO BUG: 500 вместо 400 при неправильном query roles
                ),
            ],
            ids=[
                "pageSize < 1",
                "page < 1",
                "pageSize > 20",
                "wrong createdAt query",
                "wrong roles query format",
                "wrong roles query",
            ],
        ),
    )
    get_user_wrong_locator = TestInitials(
        title="Получение пользователя по неправильному локатору [{param_id}]",
        parameters=TestParameters(
            arg_names="user_id, expected_status",
            arg_values=[
                (DataGenerator.too_big_number(), HTTPStatus.OK),
                (DataGenerator.too_big_number() * -1, HTTPStatus.OK),
                (-1, HTTPStatus.OK),
                (fake.email(), HTTPStatus.OK),
            ],
            ids=[
                "Too big number of user_id",
                "Too big negative number of user_id",
                "user_id = -1",
                "random email",
            ],
        ),
    )
    get_user_wrong_session_role = TestInitials(
        title='Получение пользователя из-под неправильной ролёвки "{param_id}"',
        parameters=TestParameters(
            arg_names="parameter_session, expected_status, expected_message",
            arg_values=[
                (
                    "noauth_session",
                    HTTPStatus.UNAUTHORIZED,
                    ServerErrorMessages.AccessErrors.UNAUTHORIZED,
                ),
                (
                    "new_user_common_session",
                    HTTPStatus.FORBIDDEN,
                    ServerErrorMessages.AccessErrors.FORBIDDEN_RESOURCE,
                ),
            ],
            ids=["common user", "no_auth"],
            indirect=["parameter_session"],
        ),
    )
