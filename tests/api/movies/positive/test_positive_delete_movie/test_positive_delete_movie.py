from http import HTTPStatus
import allure
from tests.testconstants import QA_ILYA_INITIALS
from tests.api.movies.testconstants import allure_feature
from tools.assert_response_message import assert_response_message
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив тест удаление фильма")
@allure.description(
    """
    Тестирование позитивного сценария удаления фильма, созданного через фикстуру.
    """
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestMoviePositiveDelete:
    def test_delete_movie(self, create_movie, su_session, db_helper):
        expected_message = "Фильм не найден"
        movie_id = create_movie.response_model.id
        movie_name = create_movie.response_model.name

        su_session.movies_api.delete_movie(movie_id)
        response = su_session.movies_api.get_movie(
            movie_id, expected_status=HTTPStatus.NOT_FOUND
        )
        db_response = db_helper.get_movie_by_name(movie_name)

        assert_response_message(
            reason="Удалили фильм, пытаемся получить его через GET, проверяем полученный ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="equal",
            assertion_message="После удаления фильма, нет сообщения в ответе о том что он не найден",
        )
        assert db_response is None, "Ручка удалила фильм, но в БД он остался"
