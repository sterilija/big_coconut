from http import HTTPStatus

from faker import Faker

from constants.error_messages import ServerErrorMessages, RequiredTypes
from tests.testconstants import TestInitials, TestParameters

allure_file_description = """
    Тестирование негативных сценариев получения фильма.
    Тесты, присутствующе в этом файле:
    1. test_get_movie_wrong_id - получение фильма с неправильным ID
    2. (парам.) test_get_movie_negative_boundary_ids - получение фильма с ID на границах диапазона
    3. test_get_movie_string_id - получение фильма используя слово вместо ID
    4. (парам.) test_get_movies_list_wrong_query_type -  получение фильма с неправильными query-параметрами
    5. (парам.) test_get_movies_list_wrong_pagination -  получение фильма с нарушением законов пагинации
    6. (парам.) test_get_movies_list_wrong_price -  получение фильма, указав неправильную цену
    """

fake = Faker()

XFAIL_REASON_MSG = "Ответ 500, который приходит вместо 404 (баг бэкенда)"
STP_ERROR_COMPARISON_MSG = "Проверяем что ругань в ответе соответствует ожидаемой"
NOT_FOUND_MSG = ServerErrorMessages.Film_errors.FILM_NOT_FOUND
WRONG_DATA_MSG = ServerErrorMessages.WRONG_DATA
NON_EXISTING_MOVIE_GET_EXCEPTION_MSG = (
    "Неверное сообщение в ответе при получении не существующего фильма"
)


class TestsList:
    get_movie_wrong_id = TestInitials(
        title="Получение фильма с неправ. ID",
        description=(
            """
        Тут берётся огромный номер в качестве ID, который, я надеюсь, без перезапуска стенда, мы никогда не достигнем
        А ещё здесь вместо ожидаемого 404, вылезает 500
        """
        ),
    )
    get_movie_negative_boundary_ids = TestInitials(
        title="(парам.) Получение фильма через ID на краях границ диапазона, [{param_id}]",
        parameters=TestParameters(
            arg_names="movie_id, expected_message, expected_status, assertion_message",
            arg_values=[
                (
                    0,
                    NOT_FOUND_MSG,
                    HTTPStatus.NOT_FOUND,
                    NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
                ),
                (
                    -500,
                    NOT_FOUND_MSG,
                    HTTPStatus.NOT_FOUND,
                    NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
                ),
                (
                    fake.random_int(max=0, min=-500),
                    NOT_FOUND_MSG,
                    HTTPStatus.NOT_FOUND,
                    NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
                ),
            ],
            ids=["id: 0", "id: -500", "random id: (max=0, min=-500)"],
        ),
    )
    get_movie_string_id = TestInitials(
        title="Получение фильма с рандомным стринговым словом вместо ID",
    )
    get_movies_list_wrong_query_type = TestInitials(
        title="(парам.) Получение фильма с неправ. query-параметрами, [{param_id}]",
        parameters=TestParameters(
            arg_names="query, expected_message",
            arg_values=[
                (
                    {"pageSize": fake.random_int(max=0)},
                    ServerErrorMessages.field_has_minimum_amount("pageSize", 1),
                ),
                (
                    {"pageSize": fake.word()},
                    ServerErrorMessages.field_must_be_type(
                        "pageSize", RequiredTypes.NUMBER
                    ),
                ),
                (
                    {"page": fake.random_int(max=0)},
                    ServerErrorMessages.field_has_minimum_amount("page", 1),
                ),
                (
                    {"page": fake.word()},
                    ServerErrorMessages.field_must_be_type(
                        "page", RequiredTypes.NUMBER
                    ),
                ),
                (
                    {"minPrice": -1},
                    ServerErrorMessages.field_has_minimum_amount("minPrice", 1),
                ),
                (
                    {"minPrice": fake.boolean()},
                    ServerErrorMessages.field_must_be_type(
                        "minPrice", RequiredTypes.NUMBER
                    ),
                ),
                # ({"locations": ["kompot", 123]}, "Поле locations неправ. типа"),TODO BUG: Нет реакции на поле locations
                (
                    {"genreId": fake.random_int(max=0)},
                    ServerErrorMessages.field_has_minimum_amount("genreId", 1),
                ),
                (
                    {"genreId": fake.word()},
                    ServerErrorMessages.field_must_be_type(
                        "genreId", RequiredTypes.NUMBER
                    ),
                ),
            ],
            ids=[
                "pageSize < 1",
                "pageSize wrong type",
                "page < 1",
                "page wrong type",
                "minPrice < 1",
                "minPrice wrong type",
                "genreId < 1",
                "genreId wrong type",
            ],
        ),
    )
    get_movies_list_wrong_pagination = TestInitials(
        title="(парам.) Получение фильма с неправильной пагинацией, [{param_id}]",
        parameters=TestParameters(
            arg_names="query, expected_message, assertion_message",
            arg_values=[
                (
                    {"pageSize": fake.random_int(max=0), "page": 1},
                    ServerErrorMessages.field_has_minimum_amount("pageSize", 1),
                    "Неверное сообщение в ответе при попытке получить список фильмов с pageSize < 1",
                ),
                (
                    {"pageSize": 1, "page": fake.random_int(max=0)},
                    ServerErrorMessages.field_has_minimum_amount("page", 1),
                    "Неверное сообщение в ответе при попытке получить список фильмов с page < 1",
                ),
                (
                    {
                        "pageSize": fake.random_int(min=21),
                        "page": fake.random_int(min=1, max=30),
                    },
                    ServerErrorMessages.field_has_maximum_amount("pageSize", 20),
                    "Неверное сообщение в ответе при попытке получить список фильмов с pageSize > 20",
                ),
            ],
            ids=[
                "pageSize < 1",
                "page < 1",
                "pageSize > 20",
            ],
        ),
    )
    get_movies_list_wrong_price = TestInitials(
        title="(парам.) Получение фильма с неправильным query-параметром цены, [{param_id}]",
        parameters=TestParameters(
            arg_names="query, expected_message, assertion_message",
            arg_values=[
                (
                    {
                        "minPrice": fake.random_int(min=531, max=1000000),
                        "maxPrice": fake.random_int(min=1, max=531),
                    },
                    ServerErrorMessages.field_must_be_less_than("minPrice", "maxPrice"),
                    "Неверное сообщение в ответе при попытке получить список фильмов с minPrice > maxPrice",
                ),
                (
                    {"maxPrice": 2147483649},
                    WRONG_DATA_MSG,
                    "Неверное сообщение в ответе при попытке получить список фильмов со слишком большой ценой",
                ),
                (
                    {
                        "minPrice": fake.random_int(max=0),
                        "maxPrice": fake.random_int(max=0),
                    },
                    ServerErrorMessages.field_must_be_less_than("minPrice", "maxPrice"),
                    "Неверное сообщение в ответе при попытке получить список фильмов с minPrice < 1",
                ),
            ],
            ids=["minPrice > maxPrice", "too_big_number", "minPrice < 1"],
        ),
    )
