from http import HTTPStatus

from faker import Faker

from constants.error_messages import ServerErrorMessages, RequiredTypes
from models.api.movies_model import Location
from tests.testconstants import TestInitials, TestParameters
from tools.data_generator import DataGenerator

allure_file_description = """
    Тестирование негативных сценариев редактирования фильма.
    Тесты, присутствующе в этом файле:
    1. test_edit_movie_wrong_id - редактирование фильма с неправ. id
    2. (парам.) test_edit_movie_wrong_params - редактирование фильма с неправ. параметрами
    3. (парам.) test_edit_movie_wrong_role - редактирование фильма, используя неправильную ролёвку
"""

fake = Faker()

locations_list = [e.value for e in Location]
generate_movie = DataGenerator.new_movie
FILM_NOT_FOUND_MSG = ServerErrorMessages.Film_errors.FILM_NOT_FOUND
STP_ERROR_COMPARISON_MSG = "Проверяем что ругань в ответе соответствует ожидаемой"
STP_CHECK_FILM_NO_CHANGES = "Проверяем что в нашем фильме не произошло изменений"


class TestsList:
    edit_movie_wrong_id = TestInitials(
        title="(парам.) Редактирование фильма с неправильным ID [{param_id}]",
        description="Тут берётся огромный номер в качестве ID, который, я надеюсь, без перезапуска стенда, мы никогда не достигнем",
    )
    edit_movie_wrong_params = TestInitials(
        title="(парам.) Редактирование фильма с неправильным параметром, [{param_id}]",
        parameters=TestParameters(
            arg_names="payload, expected_status, expected_message",
            arg_values=[
                (
                    generate_movie(name=[]),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "name", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(name=None),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.WRONG_DATA,
                ),
                (
                    generate_movie(name=""),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.WRONG_DATA,
                ),
                (
                    generate_movie(price=fake.word()),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "price", RequiredTypes.NUMBER
                    ),
                ),
                (
                    generate_movie(price=0),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_not_less_than("price", 1),
                ),
                (
                    generate_movie(price=fake.random_int(max=0)),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_not_less_than("price", 1),
                ),
                (
                    generate_movie(price=2147483649),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.WRONG_DATA,
                ),
                (
                    generate_movie(description=[]),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "description", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(location=fake.random_int()),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "location", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(location=fake.word()),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_one_of_eng(
                        "location", locations_list
                    ),
                ),
                (
                    generate_movie(published=fake.random_int()),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "published", RequiredTypes.BOOL
                    ),
                ),
                (
                    generate_movie(genreId=fake.word()),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_must_be_type(
                        "genreId", RequiredTypes.NUMBER
                    ),
                ),
                (
                    generate_movie(genreId=0),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_has_minimum_amount("genreId", 1),
                ),
                (
                    generate_movie(genreId=fake.random_int(max=0)),
                    HTTPStatus.BAD_REQUEST,
                    ServerErrorMessages.field_has_minimum_amount("genreId", 1),
                ),
            ],
            ids=[
                "Wrong type name",
                "Wrong type name",
                "Empty-string name",
                "Wrong type price",
                "Wrong price number",
                "Wrong price number",
                "Wrong price number",
                "Wrong type description",
                "Wrong type location",
                "Wrong location",
                "Wrong type published",
                "Wrong type genreId",
                "Wrong genreId number",
                "Wrong genreId number",
            ],
        ),
    )
    edit_movie_wrong_role = TestInitials(
        title="(парам.) Редактирование фильма из-под неправильной ролёвки, [{param_id}]",
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
            ids=["Unauthorized", "Common User"],
            indirect=["parameter_session"],
        ),
    )
