import pytest

from models.api.movies_model import CreateMovieDto
from tools.compare_dicts_by_keys import compare_dicts_by_keys
from tools.data_generator import DataGenerator
import allure

from positive_edit_movie_constants import (
    allure_file_description,
    NEW_DATA_TO_GET_MISMATCH_MSG,
    NEW_DATA_TO_RESPONSE_MISMATCH_MSG,
    NEW_DATA_TO_DB_MISMATCH_MSG,
    TestsList,
)
from tests.testconstants import QA_ILYA_INITIALS
from tests.api.movies.testconstants import allure_feature
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив тест редактирование фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestMoviePositiveUpdate:
    @allure.title(TestsList.update_movie_full.title)
    def test_update_movie_full(self, create_movie, su_session, db_helper):
        movie_id = create_movie.response_model.id
        patch_payload = DataGenerator.new_movie()

        db_response_before = db_helper.get_movie_by_id(movie_id)
        patch_response = su_session.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=patch_payload,
        )
        patch_dict = patch_response.model_dump(mode="python")
        get_response = su_session.movies_api.get_movie(movie_id)
        get_dict = get_response.model_dump(mode="python")
        db_helper.db_session.expire_all()
        db_response = db_helper.get_movie_by_id(movie_id)
        db_response_after = db_response.convert_to_dict()

        assert db_response_before is not None, (
            "Фильм через фикстуру создан, а в БД его нет"
        )
        compare_dicts_by_keys(
            patch_payload,
            patch_dict,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_RESPONSE_MISMATCH_MSG,
            reason="Проверяем что payload в POST соответствует вернувшемуся ответу после POST",
        )
        compare_dicts_by_keys(
            patch_payload,
            get_dict,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_GET_MISMATCH_MSG,
            reason="Сверяем данные фильма после редактирования",
        )
        compare_dicts_by_keys(
            db_response_after,
            patch_payload,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_DB_MISMATCH_MSG,
        )

    @allure.title(TestsList.update_movie_partial.title)
    @pytest.mark.parametrize(
        argnames=TestsList.update_movie_partial.parameters.arg_names,
        argvalues=TestsList.update_movie_partial.parameters.arg_values,
        ids=TestsList.update_movie_partial.parameters.ids,
    )
    def test_update_movie_partial(
        self, db_helper, create_movie, su_session, field_key, field_value
    ):
        movie_id = create_movie.response_model.id
        patch_payload = {field_key: field_value}
        dict_expected = create_movie.payload | patch_payload

        db_response_before = db_helper.get_movie_by_id(movie_id)
        patch_data = su_session.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=patch_payload,
        )
        patch_dict = patch_data.model_dump(mode="python")
        db_helper.db_session.expire_all()
        db_response = db_helper.get_movie_by_id(movie_id)
        db_response_after = db_response.convert_to_dict()
        get_data = su_session.movies_api.get_movie(movie_id)
        get_dict = get_data.model_dump(mode="python")

        assert db_response_before is not None, (
            "Фильм через фикстуру создан, а в БД его нет"
        )
        compare_dicts_by_keys(
            patch_dict,
            dict_expected,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_RESPONSE_MISMATCH_MSG,
        )
        compare_dicts_by_keys(
            patch_dict,
            get_dict,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_GET_MISMATCH_MSG,
        )
        compare_dicts_by_keys(
            patch_dict,
            db_response_after,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_DB_MISMATCH_MSG,
        )
