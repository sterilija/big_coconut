import pytest
import allure

from tools.assert_response_message import assert_response_message
from tools.compare_dicts_by_keys import compare_dicts_by_keys
from tools.data_generator import DataGenerator
from http import HTTPStatus
from models.api.movies_model import CreateMovieDto
from negative_edit_movie_constants import (
    allure_file_description,
    FILM_NOT_FOUND_MSG,
    generate_movie,
    TestsList,
)
from tests.api.movies.testconstants import allure_feature
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест редактирование фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestMovieNegativeEdit:
    @allure.title(TestsList.edit_movie_wrong_id.title)
    @allure.description(TestsList.edit_movie_wrong_id.description)
    def test_edit_movie_wrong_id(self, su_session):
        expected_message = FILM_NOT_FOUND_MSG
        fake_id = DataGenerator.too_big_number()
        new_json = generate_movie()

        response = su_session.movies_api.edit_movie(
            movie_id=fake_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.NOT_FOUND,
        )

        assert_response_message(
            reason="Попытались отредактировать несуществующий фильм, проверяем ответ",
            response_message=response.message,
            expected_message=expected_message,
            checking_type="equal",
            assertion_message="Неверное сообщение в ответе при редактировании несуществующего фильма",
        )

    @allure.title(TestsList.edit_movie_wrong_params.title)
    @pytest.mark.parametrize(
        argnames=TestsList.edit_movie_wrong_params.parameters.arg_names,
        argvalues=TestsList.edit_movie_wrong_params.parameters.arg_values,
        ids=TestsList.edit_movie_wrong_params.parameters.ids,
    )
    def test_edit_movie_wrong_params(
        self, su_session, create_movie, expected_message, payload, expected_status
    ):
        movie_id = create_movie.response_model.id

        edit_response = su_session.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=payload,
            expected_status=expected_status,
        )
        get_response = su_session.movies_api.get_movie(movie_id)

        assert_response_message(
            reason="Попытались отредактировать фильм, введя неправ. параметры, проверяем ответ",
            response_message=edit_response.message,
            expected_message=expected_message,
            checking_type="in",
            assertion_message="Неправильное сообщение в ответе при неправильном изменении полей",
        )
        compare_dicts_by_keys(
            reason="Попытались отредактировать фильм, введя неправ. параметры,"
            "получив его, проверяем, что ничего не поменялось",
            negative=True,
            dict_original=payload,
            dict_expected=get_response.model_dump(mode="json"),
            keys=list(payload.keys()),
            exception_message=(
                "Неправильные поля при изменении фильма вызвали 400, но апдейт этих полей всё равно произошёл"
            ),
        )

    @allure.title(TestsList.edit_movie_wrong_role.title)
    @pytest.mark.slow
    @pytest.mark.parametrize(
        argnames=TestsList.edit_movie_wrong_role.parameters.arg_names,
        argvalues=TestsList.edit_movie_wrong_role.parameters.arg_values,
        ids=TestsList.edit_movie_wrong_role.parameters.ids,
        indirect=TestsList.edit_movie_wrong_role.parameters.indirect,
    )
    def test_edit_movie_wrong_role(
        self, parameter_session, create_movie, expected_status, expected_message
    ):
        movie_id = create_movie.response_model.id
        new_json = generate_movie()

        edit_response = parameter_session.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expected_status=expected_status,
        )
        get_response = parameter_session.movies_api.get_movie(movie_id)

        assert_response_message(
            reason="Попытались изменить фильм без авторизации, проверяем ответ",
            response_message=edit_response.message,
            expected_message=expected_message,
            checking_type="equal",
            assertion_message="Неправильный ответ в сообщении при изменении полей без авторизации",
        )
        compare_dicts_by_keys(
            reason="Попытались отредактировать фильм, из-под неправ. роли,"
            "получив его, проверяем, что ничего не поменялось",
            negative=True,
            dict_original=new_json,
            dict_expected=get_response.model_dump(mode="json"),
            keys=CreateMovieDto.model_fields.keys(),
            exception_message=(
                "Пользователь без соотв. роли смог изменить данные фильма"
            ),
        )
