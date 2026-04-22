import allure
import pytest
from http import HTTPStatus
from tools.assert_response_message import assert_response_message
from tools.data_generator import DataGenerator
from constants.error_messages import ServerErrorMessages
from models.api.movies_model import Location

from negative_create_movie_constants import (
    TestsList,
    allure_file_description,
    generate_movie,
    EMPTY_BODY_EXPECTED_MESSAGE,
)

from tests.api.movies.testconstants import allure_feature
from tests.testconstants import allure_epic

locations_list = [e.value for e in Location]


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест создание фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestMovieNegativeCreate:
    @allure.title(TestsList.create_movie_empty_body.title)
    @allure.description(TestsList.create_movie_empty_body.description)
    def test_create_movie_empty_body(self, su_session):
        response = su_session.movies_api.create_movie(
            data_json={}, expected_status=HTTPStatus.BAD_REQUEST
        )

        assert_response_message(
            reason="Попытались создать фильм с пустым телом, проверяем ответ",
            response_message=response.message,
            expected_message=EMPTY_BODY_EXPECTED_MESSAGE,
            checking_type="equal",
            assertion_message="Ответ при создании пустотелого фильма не соответствует ожидаемому",
        )

    @allure.title(TestsList.create_movie_name_already_exists.title)
    def test_create_movie_name_already_exists(self, create_movie, su_session):
        expected_message = (
            ServerErrorMessages.Film_errors.FILM_WITH_THE_NAME_ALREADY_EXISTS
        )
        movie_name = create_movie.response_model.name
        new_movie_json = generate_movie(name=movie_name)

        response = su_session.movies_api.create_movie(
            data_json=new_movie_json, expected_status=HTTPStatus.CONFLICT
        )

        assert_response_message(
            reason="Попытались создать фильм с тем-же именем, проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="equal",
            assertion_message="Неправильный ответ при попытке создать фильм с уже существующим именем",
        )

    @pytest.mark.parametrize(
        argnames=TestsList.create_movie_wrong_field_type.parameters.arg_names,
        argvalues=TestsList.create_movie_wrong_field_type.parameters.arg_values,
        ids=TestsList.create_movie_wrong_field_type.parameters.ids,
    )
    def test_create_movie_wrong_field_type(self, su_session, payload, expected_message):
        response = su_session.movies_api.create_movie(
            payload, expected_status=HTTPStatus.BAD_REQUEST
        )

        assert_response_message(
            reason="Попытались создать фильм с неправ. полем, проверяем ответ",
            expected_message=expected_message,
            response_message=response.message,
            checking_type="in",
            assertion_message="Ответ при создании фильма с неправ. полями не соответствует ожидаемому",
        )

    @allure.title(TestsList.create_movie_wrong_role.title)
    @pytest.mark.slow
    @pytest.mark.parametrize(
        argnames=TestsList.create_movie_wrong_role.parameters.arg_names,
        argvalues=TestsList.create_movie_wrong_role.parameters.arg_values,
        ids=TestsList.create_movie_wrong_role.parameters.ids,
        indirect=TestsList.create_movie_wrong_role.parameters.indirect,
    )
    def test_create_movie_wrong_role(
        self, parameter_session, expected_status, expected_message
    ):
        new_movie = generate_movie()

        response = parameter_session.movies_api.create_movie(
            data_json=new_movie, expected_status=expected_status
        )

        assert_response_message(
            reason="Попытались создать фильм из-под неправ. роли, проверяем ответ",
            expected_message=expected_message,
            response_message=response.message,
            checking_type="equal",
        )

    @allure.title(TestsList.create_movie_attack_xss.title)
    @pytest.mark.xfail  # TODO разрабам: Сделать запрет или экранирование XSS-атак
    def test_create_movie_attack_xss(self, su_session):
        with allure.step("Создаём фильм и встраиваем в его название JS-скрипт"):
            new_movie = DataGenerator.new_movie(
                name="<script>alert(1)</script>",
            )

        su_session.movies_api.create_movie(
            data_json=new_movie, expected_status=HTTPStatus.BAD_REQUEST
        )

    @allure.title(TestsList.create_movie_attack_sql.title)
    @pytest.mark.xfail  # TODO разрабам: Сделать запрет или экранирование SQL_injection-атак
    def test_create_movie_attack_sqli(self, su_session):
        with allure.step("Создаём фильм и встраиваем в его название SQL-запрос"):
            new_movie = DataGenerator.new_movie(
                name="' OR 1=1",
            )

        su_session.movies_api.create_movie(
            data_json=new_movie, expected_status=HTTPStatus.BAD_REQUEST
        )
