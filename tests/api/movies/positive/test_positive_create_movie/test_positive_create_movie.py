from models.api.movies_model import CreateMovieDto
from http import HTTPStatus

from tests.api.movies.testconstants import allure_feature
from tools.compare_dicts_by_keys import compare_dicts_by_keys
from tools.data_generator import DataGenerator
import allure
from positive_create_movie_constants import allure_file_description, TestsList
from tests.testconstants import QA_ILYA_INITIALS
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив теста создание фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestMoviePositiveCreate:
    @allure.title(TestsList.create_movie_fixture_su.title)
    def test_create_movie_fixture_su(self, create_movie, su_session):
        movie_id = create_movie.response_model.id

        movie_response = su_session.movies_api.get_movie(
            movie_id, expected_status=HTTPStatus.OK
        )

        compare_dicts_by_keys(
            reason="Получили (через GET) фильм, созданный фикстурой,"
            "проверяем соответствие тому что мы отправляли при создании",
            dict_original=create_movie.payload,
            dict_expected=movie_response.model_dump(mode="json"),
            keys=CreateMovieDto.model_fields.keys(),
            exception_message="Данные в отправленных полях фильма не соответствуют данным из ответа при его получении",
        )
        compare_dicts_by_keys(
            reason="Получили (через GET) данные фильма, созданный фикстурой,"
            "проверяем соответствие тому что получили при создании",
            dict_original=create_movie.response_model.model_dump(mode="json"),
            dict_expected=movie_response.model_dump(mode="json"),
            keys=create_movie.response_model.model_fields.keys(),
            exception_message="Данные в ответе после создания фильма не соответствуют данным при его получении",
        )

    @allure.title(TestsList.create_movie_su.title)
    def test_create_movie_su(self, su_session, db_helper):
        movie_json = DataGenerator.new_movie()

        db_response_before_creation = db_helper.get_movie_by_name(
            movie_json.get("name")
        )
        creation_response = su_session.movies_api.create_movie(movie_json)
        get_response = su_session.movies_api.get_movie(creation_response.id)
        db_response = db_helper.get_movie_by_name(get_response.name)
        comparable_keys = db_response.get_column_names()
        comparable_keys.remove("createdAt")
        creation_response_dict = creation_response.model_dump(mode="json")
        get_response_dict = get_response.model_dump(mode="json")
        db_response_dict = db_response.convert_to_dict()

        assert db_response_before_creation is None, (
            "Фильм не создали, а в БД он уже есть"
        )
        assert creation_response_dict == get_response_dict, (
            "Данные ответа при создании фильма не соответствуют данным ответа при его получении"
        )
        compare_dicts_by_keys(
            reason="Получили фильм из БД и через GET из API, проверяем схожесть этих ответов",
            dict_original=get_response_dict,
            dict_expected=db_response_dict,
            keys=comparable_keys,
            exception_message="Данные в ответе сервера отличаются от данных в БД",
        )
