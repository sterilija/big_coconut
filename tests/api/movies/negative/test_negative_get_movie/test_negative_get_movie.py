import pytest
import allure

from tools.assert_response_message import assert_response_message
from tools.data_generator import DataGenerator
from http import HTTPStatus
from tests.api.movies.testconstants import allure_feature
from negative_get_movie_constants import (
    allure_file_description,
    NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
    NOT_FOUND_MSG,
    fake,
    TestsList,
    XFAIL_REASON_MSG,
)
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест получение фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestMovieNegativeGet:
    @allure.title(TestsList.get_movie_wrong_id.title)
    @allure.description(TestsList.get_movie_wrong_id.description)
    @pytest.mark.xfail(reason=XFAIL_REASON_MSG)
    def test_get_movie_wrong_id(self, su_session):
        movie_id = DataGenerator.too_big_number()

        response = su_session.movies_api.get_movie(
            movie_id=movie_id, expected_status=HTTPStatus.NOT_FOUND
        )

        assert_response_message(
            reason="Попытались получить фильм по неправ. ID, проверяем ответ",
            response_message=response.message,
            expected_message=NOT_FOUND_MSG,
            checking_type="equal",
            assertion_message=NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
        )

    @allure.title(TestsList.get_movie_negative_boundary_ids.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movie_negative_boundary_ids.parameters.arg_names,
        argvalues=TestsList.get_movie_negative_boundary_ids.parameters.arg_values,
        ids=TestsList.get_movie_negative_boundary_ids.parameters.ids,
    )
    def test_get_movie_negative_boundary_ids(
        self, su_session, movie_id, expected_message, expected_status, assertion_message
    ):
        response = su_session.movies_api.get_movie(
            movie_id=movie_id, expected_status=expected_status
        )

        assert_response_message(
            reason="Попытались получить фильм по неправ. ID (рамки отрицательного диапазона), проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="equal",
            assertion_message="Ругань в ответе от сервера при попытке изменить фильм с неверным ID не соотв. ожидаемой",
        )

    @allure.title(TestsList.get_movie_string_id.title)
    @pytest.mark.xfail(reason=XFAIL_REASON_MSG)
    def test_get_movie_string_id(self, su_session):
        wrong_id = fake.word()

        response = su_session.movies_api.get_movie(
            movie_id=wrong_id, expected_status=HTTPStatus.NOT_FOUND
        )

        assert_response_message(
            reason="Попытались получить фильм по слову вместо ID, проверяем ответ",
            response_message=response.message,
            expected_message=NOT_FOUND_MSG,
            checking_type="equal",
            assertion_message=NON_EXISTING_MOVIE_GET_EXCEPTION_MSG,
        )

    @allure.title(TestsList.get_movies_list_wrong_query_type.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_wrong_query_type.parameters.arg_names,
        argvalues=TestsList.get_movies_list_wrong_query_type.parameters.arg_values,
        ids=TestsList.get_movies_list_wrong_query_type.parameters.ids,
    )
    def test_get_movies_list_wrong_query_type(
        self, su_session, query, expected_message
    ):
        response = su_session.movies_api.get_movies_list(
            query=query, expected_status=HTTPStatus.BAD_REQUEST
        )

        assert_response_message(
            reason="Попытались получить список фильмов с неправильными query-параметрами, проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="in",
            assertion_message="Неверное сообщение в ответе при попытке получить фильм с неправильными query-параметрами",
        )

    @allure.title(TestsList.get_movies_list_wrong_pagination.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_wrong_pagination.parameters.arg_names,
        argvalues=TestsList.get_movies_list_wrong_pagination.parameters.arg_values,
        ids=TestsList.get_movies_list_wrong_pagination.parameters.ids,
    )
    def test_get_movies_list_wrong_pagination(
        self, su_session, query, expected_message, assertion_message
    ):
        response = su_session.movies_api.get_movies_list(
            query=query, expected_status=HTTPStatus.BAD_REQUEST
        )

        assert_response_message(
            reason="Попытались получить список фильмов с неправ. пагинацией, проверяем ответ",
            expected_message=expected_message,
            response_message=response.message,
            checking_type="in",
            assertion_message=assertion_message,
        )

    @allure.title(TestsList.get_movies_list_wrong_price.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_wrong_price.parameters.arg_names,
        argvalues=TestsList.get_movies_list_wrong_price.parameters.arg_values,
        ids=TestsList.get_movies_list_wrong_price.parameters.ids,
    )
    def test_get_movies_list_wrong_price(
        self, su_session, query, expected_message, assertion_message
    ):
        response = su_session.movies_api.get_movies_list(
            query=query, expected_status=HTTPStatus.BAD_REQUEST
        )

        assert_response_message(
            reason="Попытались получить список фильмовЮ, указав неправ. цену, проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="in",
            assertion_message=assertion_message,
        )
