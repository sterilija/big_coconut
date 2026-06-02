from http import HTTPStatus

from constants.error_messages import ServerErrorMessages
from tests.testconstants import TestInitials, TestParameters

NOT_FOUND_MSG = ServerErrorMessages.Film_errors.FILM_NOT_FOUND
NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG = (
    "Неверный ответ при удалении не существующего фильма"
)
STP_ERROR_COMPARISON_MSG = "Проверяем что ругань в ответе соответствует ожидаемой"

allure_file_description = """
    Тестирование негативных сценариев удаления фильма.
    Тесты, присутствующе в этом файле:
    1. test_delete_movie_wrong_id - Удаление фильма с неправильным ID
    2. test_delete_movie_same_id_twice - Удаление фильма два (2) раза
    3. (парам.) test_delete_movie_wrong_role -  удаление фильма из-под неправильной роли
"""


class TestsList:
    delete_movie_wrong_id = TestInitials(
        title="Удаление фильма с неправ. ID",
        description=(
            """
            Тут берётся огромный номер в качестве ID, который, я надеюсь, без перезапуска стенда, мы никогда не достигнем
            """
        ),
    )
    delete_movie_same_id_twice = TestInitials(
        title="Удаление фильма два раза",
        description=(
            """
            Тут мы берём ID созданного фикстурой фильма и пытаемся удалить его 2 раза
            """
        ),
    )
    delete_movie_wrong_role = TestInitials(
        title="(парам.) Удаление фильма из-под неправильной ролёвки, [{param_id}]",
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
