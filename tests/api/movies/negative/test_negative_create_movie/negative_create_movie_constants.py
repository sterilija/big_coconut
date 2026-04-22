from http import HTTPStatus
from tests.testconstants import TestInitials, TestParameters


from tools.data_generator import DataGenerator
from models.api.movies_model import Location
from constants.error_messages import ServerErrorMessages, RequiredTypes
from faker import Faker

generate_movie = DataGenerator.new_movie
locations_list = [e.value for e in Location]

fake = Faker()
allure_file_description = """
    Тестирование негативных сценариев создания фильма.
    Тесты, присутствующе в этом файле:
    1. test_create_movie_empty_body - Создание фильма с пустым телом
    2. test_create_movie_name_already_exists - Создание фильма с уже существующим именем
    3. (парам.) test_create_movie_wrong_field_type -  Создание фильма с указанием неправильных данных в полях
    4. (парам.) test_create_movie_wrong_role -  Создание фильма, используя неправильную ролёвку
    5. (парам.) (xfail) test_create_movie_attack_xss -  Создание фильма, используя XSS-атаку 
    6. (парам.) (xfail) test_create_movie_attack_sqli -  Создание фильма, используя SQL-инъекцию 
    """

EMPTY_BODY_EXPECTED_MESSAGE = [
    "Поле name должно содержать не менее 3 символов",
    ServerErrorMessages.field_must_be_type("name", RequiredTypes.STRING),
    ServerErrorMessages.field_cannot_be_empty("name"),
    ServerErrorMessages.field_must_be_more_than("price", 0),
    ServerErrorMessages.field_must_be_type("price", RequiredTypes.NUMBER),
    ServerErrorMessages.field_cannot_be_empty("price"),
    "Поле description должно содержать не менее 5 символов",
    ServerErrorMessages.field_must_be_type("description", RequiredTypes.STRING),
    ServerErrorMessages.field_cannot_be_empty("description"),
    ServerErrorMessages.field_must_be_one_of_rus("location", locations_list),
    ServerErrorMessages.field_must_be_type("location", RequiredTypes.STRING),
    ServerErrorMessages.field_cannot_be_empty("location"),
    ServerErrorMessages.field_must_be_type("published", RequiredTypes.BOOL),
    ServerErrorMessages.field_cannot_be_empty("published"),
    ServerErrorMessages.field_must_be_type("genreId", RequiredTypes.INTEGER),
    ServerErrorMessages.field_must_be_type("genreId", RequiredTypes.NUMBER),
    ServerErrorMessages.field_cannot_be_empty("genreId"),
]


class TestsList:
    create_movie_empty_body = TestInitials(
        title="Создание фильма с пустым телом",
        description="В случае попытки создать фильм с пустотелым запросом,"
        "сервер должен отдать нам целую кучу жалоб на неправильные"
        "поля",
        parameters=None,
    )
    create_movie_name_already_exists = TestInitials(
        "Создание фильма с уже существующим названием"
    )
    create_movie_wrong_field_type = TestInitials(
        title="(парам.) Создание фильма с неправ. значением в поле, [{param_id}]",
        description="тут создаём разные фильмы с неправильным значением в полях"
        "через параметризацию, во всех итерациях ожидается ответ 400",
        parameters=TestParameters(
            arg_names="payload, expected_message",
            arg_values=[
                (
                    generate_movie(name=None),
                    ServerErrorMessages.field_cannot_be_empty("name"),
                ),
                (
                    generate_movie(name=[]),
                    ServerErrorMessages.field_must_be_type(
                        "name", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(name=""),
                    ServerErrorMessages.field_cannot_be_empty("name"),
                ),
                (
                    generate_movie(price=fake.word()),
                    ServerErrorMessages.field_must_be_type(
                        "price", RequiredTypes.NUMBER
                    ),
                ),
                (generate_movie(price=2147483649), ServerErrorMessages.WRONG_DATA),
                (
                    generate_movie(description=[]),
                    ServerErrorMessages.field_must_be_type(
                        "description", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(description=None),
                    ServerErrorMessages.field_must_be_type(
                        "description", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(location=fake.random_int()),
                    ServerErrorMessages.field_must_be_type(
                        "location", RequiredTypes.STRING
                    ),
                ),
                (
                    generate_movie(location=fake.word()),
                    ServerErrorMessages.field_must_be_one_of_rus(
                        "location", locations_list
                    ),
                ),
                (
                    generate_movie(published=fake.word()),
                    ServerErrorMessages.field_must_be_type(
                        "published", RequiredTypes.BOOL
                    ),
                ),
                (
                    generate_movie(genreId=fake.word()),
                    ServerErrorMessages.field_must_be_type(
                        "genreId", RequiredTypes.NUMBER
                    ),
                ),
                (
                    generate_movie(genreId=fake.random_int(max=0)),
                    ServerErrorMessages.field_must_be_more_than("genreId", 0),
                ),
            ],
            ids=[
                "Empty name",
                "Wrong type name",
                "Empty-string name",
                "Wrong type price",
                "Wrong price number",
                "Wrong type description",
                "Empty description",
                "Wrong type location",
                "Wrong location name",
                "Wrong type published",
                "Wrong type genreId",
                "Wrong genreId number",
            ],
        ),
    )
    create_movie_wrong_role = TestInitials(
        title="(парам.) Создание фильма из-под неправильной ролёвки, [{param_id}]",
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
    create_movie_attack_xss = TestInitials("Создание фильма с XSS-атакой", None, None)
    create_movie_attack_sql = TestInitials(
        "Создание фильма с SQL-инъекцией", None, None
    )
