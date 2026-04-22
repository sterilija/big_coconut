import pytest
from tools.assert_response_message import assert_response_message
from tools.data_generator import DataGenerator
from http import HTTPStatus
import allure
from tests.api.movies.testconstants import allure_feature

from negative_delete_movie_constants import (
    TestsList,
    NOT_FOUND_MSG,
    NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG,
    allure_file_description,
)
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест удаление фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestMovieNegativeDelete:
    @allure.title(TestsList.delete_movie_wrong_id.title)
    @allure.description(TestsList.delete_movie_wrong_id.description)
    def test_delete_movie_wrong_id(self, su_session):
        movie_id = DataGenerator.too_big_number()

        response = su_session.movies_api.delete_movie(
            movie_id=movie_id, expected_status=HTTPStatus.NOT_FOUND
        )

        assert_response_message(
            reason="Удалили несущ. фильм, проверяем ответ",
            response_message=response.message,
            expected_message=NOT_FOUND_MSG,
            checking_type="equal",
            assertion_message=NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG,
        )

    @allure.title(TestsList.delete_movie_same_id_twice.title)
    @allure.description(TestsList.delete_movie_same_id_twice.description)
    def test_delete_movie_same_id_twice(self, su_session, create_movie):
        movie_id = create_movie.response_model.id

        su_session.movies_api.delete_movie(movie_id)
        with allure.step("удаляем ещё раз и запоминаем ответ"):
            response_second_deletion = su_session.movies_api.delete_movie(
                movie_id, expected_status=HTTPStatus.NOT_FOUND
            )
        with allure.step("Пытаемся получить удалённый фильм"):
            response_get_after_deletion = su_session.movies_api.get_movie(
                movie_id, expected_status=HTTPStatus.NOT_FOUND
            )

        assert_response_message(
            reason="Удалили тот же фильм второй раз, проверяем ответ",
            response_message=response_second_deletion.message,
            expected_message=NOT_FOUND_MSG,
            checking_type="equal",
            assertion_message=NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG,
        )
        assert_response_message(
            reason="Сделали GET фильма после удаления, проверяем ответ",
            response_message=response_get_after_deletion.message,
            expected_message=NOT_FOUND_MSG,
            checking_type="equal",
            assertion_message="неправильный ответ при получении несуществ. фильма",
        )

    @allure.title(TestsList.delete_movie_wrong_role.title)
    @pytest.mark.parametrize(
        argnames=TestsList.delete_movie_wrong_role.parameters.arg_names,
        argvalues=TestsList.delete_movie_wrong_role.parameters.arg_values,
        ids=TestsList.delete_movie_wrong_role.parameters.ids,
        indirect=TestsList.delete_movie_wrong_role.parameters.indirect,
    )
    def test_delete_movie_wrong_role(
        self, parameter_session, create_movie, expected_status, expected_message
    ):
        movie_id = create_movie.response_model.id

        response = parameter_session.movies_api.delete_movie(movie_id, expected_status)

        assert_response_message(
            reason="Попытались удалить фильм из-под неверной роли, проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="equal",
        )
