from http import HTTPStatus

from faker import Faker

from constants.error_messages import ServerErrorMessages
from tests.testconstants import TestParameters, TestInitials
from tools.data_generator import DataGenerator


allure_file_description = """
    (парам.) Тестирование негативных сценариев регистрации пользователя.
    """

new_user = DataGenerator.new_user_data
fake = Faker()

test_data = TestInitials(
    title="{param_id}",
    parameters=TestParameters(
        arg_names="payload, expected_status, expected_message, assertion_message",
        arg_values=[
            (
                new_user(email=fake.random_int()),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ServerErrorMessages.INTERNAL_ERROR,
                "Неправ. ответ при создании пользователя с неправ. типом в поле email",
            ),
            (
                new_user(email=[]),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ServerErrorMessages.INTERNAL_ERROR,
                "Неправ. ответ при создании пользователя с неправ. типом в поле email",
            ),
            (
                new_user(email=fake.word()),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.EmailErrors.INCORRECT_EMAIL,
                "Неправ. ответ при создании пользователя с неверным email",
            ),
            (
                new_user(email=""),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.EmailErrors.INCORRECT_EMAIL,
                "Неправ. ответ при создании пользователя с пустой строкой в email",
            ),
            (
                new_user(fullName=[]),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ServerErrorMessages.INTERNAL_ERROR,
                "Неправ. ответ при создании пользователя с неверным типом в поле fullName",
            ),
            (
                new_user(fullName=""),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.FIOErrors.FIO_SHOULD_NOT_BE_EMPTY,
                "Неправ. ответ при создании пользователя с пустой строкой в поле fullName",
            ),
            (
                new_user(fullName=fake.credit_card_full()),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.FIOErrors.FIO_SHOULD_HAVE_ONLY_LETTERS_AND_SPACES,
                "Неправ. ответ при создании пользователя с неправильным fullName",
            ),
            (
                new_user(fullName=fake.text(max_nb_chars=5)[:-1]),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.FIOErrors.FIO_MIN_LENGTH,
                "Неправ. ответ при создании пользователя со слишком коротким fullName",
            ),
            (
                new_user(password=[]),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ServerErrorMessages.INTERNAL_ERROR,
                "Неправ. ответ при создании пользователя с неправильным типом password",
            ),
            (
                new_user(password=fake.text(max_nb_chars=7)[:-1]),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.PasswordErrors.MIN_PASSWORD_LENGTH,
                "Неправ. ответ при создании пользователя со слишком коротким password",
            ),
            (
                new_user(password=""),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.PasswordErrors.PASSWORD_SHOULD_NOT_BE_EMPTY,
                "Неправ. ответ при создании пользователя со слишком коротким password",
            ),
            (
                new_user(password=fake.text(10)[:-1].lower()),
                HTTPStatus.BAD_REQUEST,
                ServerErrorMessages.PasswordErrors.PASSWORD_SHOULD_HAVE_CAPITALS,
                "Неправ. ответ при создании пользователя с паролем без заглавных букв",
            ),
        ],
        ids=[
            "wrong type email",
            "wrong type email",
            "wrong email",
            "empty string email",
            "wrong type fullName",
            "empty string fullName",
            "wrong fullName format",
            "too short fullName",
            "wrong type password",
            "too short password",
            "empty string password",
            "wrong password format",
        ],
    ),
)
