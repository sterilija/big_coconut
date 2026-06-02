from faker import Faker

from tests.testconstants import TestInitials, TestParameters
from tools.data_generator import DataGenerator

allure_file_description = """
    Тестирование негативных сценариев редактирования фильма.
    Тесты, присутствующе в этом файле:
    1. (парам.) test_update_movie_full - Изменение всех возможных полей фильма за раз
    2. test_update_movie_partial - Частичное редактирование полей фильма
    """

STP_CHECK_API_FILM_HAS_CHANGED = "Проверяем через API, что данные фильма обновились"
STP_CHECK_DB_FILM_HAS_CHANGED = "Проверяем через БД, что данные фильма обновились"
STP_CHECK_DB_IF_FILM_EXISTS = "Проверяем что фильм есть в БД перед его изменением"
NEW_DATA_TO_GET_MISMATCH_MSG = "Полученный фильм не соответствует сделанным изменениям"
NEW_DATA_TO_RESPONSE_MISMATCH_MSG = (
    "Ответ при изменении фильма не соответствует сделанным изменениям"
)
NEW_DATA_TO_DB_MISMATCH_MSG = (
    "Данные фильма из БД не соответствуют сделанным изменениям"
)
FILM_NOT_EXISTS_IN_DB_MSG = "Фильма нет в БД, редактирование невозможно"

fake = Faker()


class TestsList:
    update_movie_full = TestInitials(
        title="Редактирование фильма с заменой всех возможных полей"
    )
    update_movie_partial = TestInitials(
        title='Редактирование фильма с заменой поля "{param_id}"',
        parameters=TestParameters(
            arg_names="field_key, field_value",
            arg_values=[
                ("name", fake.sentence(nb_words=4, variable_nb_words=True)),
                ("price", fake.random_int()),
                ("description", fake.text(max_nb_chars=100)),
                ("location", DataGenerator.random_location()),
                ("published", fake.boolean()),
                ("genreId", fake.random_int(min=1, max=4)),
                ("imageUrl", fake.url()),
            ],
            ids=[
                "name",
                "price",
                "description",
                "location",
                "published",
                "genreId",
                "imageUrl",
            ],
        ),
    )
