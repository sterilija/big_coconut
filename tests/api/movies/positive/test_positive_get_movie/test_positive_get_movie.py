from math import ceil

from models.api.movies_model import MovieResponse
from http import HTTPStatus
import allure
import pytest

from tools.compare_dicts_by_keys import compare_dicts_by_keys
from positive_get_movie_constants import allure_file_description, TestsList, fake
from tests.testconstants import QA_ILYA_INITIALS
from tests.api.movies.testconstants import allure_feature
from tests.testconstants import allure_epic


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив тест получение фильма")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestMoviePositiveGet:
    @allure.title(TestsList.get_movie.title)
    @allure.description(TestsList.get_movie.description)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movie.parameters.arg_names,
        argvalues=TestsList.get_movie.parameters.arg_values,
        indirect=TestsList.get_movie.parameters.indirect,
    )
    def test_get_movie(self, db_helper, create_movie, parameter_session):
        movie_id = create_movie.response_model.id

        response_model = parameter_session.movies_api.get_movie(movie_id)
        response_dict = response_model.model_dump(mode="python")
        db_helper.db_session.expire_all()
        db_response = db_helper.get_movie_by_id(movie_id)
        db_response_dict = db_response.convert_to_dict()
        comparable_keys = MovieResponse.get_keys_list(
            keys_to_skip=["genre", "createdAt"]
        )

        with allure.step("Сравниваем данные созданного фильма и то что о нём получили"):
            assert response_model == create_movie.response_model, (
                "ручка get вернула не тот фильм что мы создали"
            )
        compare_dicts_by_keys(
            reason="Получили фильм через API и через БД, сравниваем результаты",
            dict_original=response_dict,
            dict_expected=db_response_dict,
            keys=comparable_keys,
            exception_message="БД вернула не те поля что мы получили через GET",
        )

    @allure.title(TestsList.get_movies_list_no_query.title)
    @allure.description(TestsList.get_movies_list_no_query.description)
    @pytest.mark.slow
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_no_query.parameters.arg_names,
        argvalues=TestsList.get_movies_list_no_query.parameters.arg_values,
        indirect=TestsList.get_movies_list_no_query.parameters.indirect,
    )
    def test_get_movies_list_no_query(self, parameter_session):
        with allure.step("Получаем список фильмов и валидируем"):
            parameter_session.movies_api.get_movies_list(query={})

    @allure.title(TestsList.get_movies_list.title)
    @pytest.mark.slow
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list.parameters.arg_names,
        argvalues=TestsList.get_movies_list.parameters.arg_values,
        indirect=TestsList.get_movies_list.parameters.indirect,
    )
    def test_get_movies_list(self, parameter_session):
        page_number = fake.random_int(max=30, min=1)
        page_size = fake.random_int(max=20, min=1)

        response_model = parameter_session.movies_api.get_movies_list(
            {"page": page_number, "pageSize": page_size}
        )
        pages_count = response_model.count
        current_size = response_model.pageSize
        expect_page_count = ceil(pages_count / current_size)
        movies_list = response_model.movies

        with allure.step("Проверяем корректность вагинации в ответе сервера"):
            assert response_model.page == page_number, (
                f"vagination page is{response_model.page}, expected {page_number}"
            )
            assert current_size == len(movies_list), (
                "vagination response has pageSize and len(movies) are not equal"
            )
            assert current_size == page_size, (
                f"vagination pageSize is {current_size}, expected {page_size}"
            )
            assert len(movies_list) == page_size, (
                f"vagination: length of movies is {len(movies_list)}, expected {page_size}"
            )
            assert response_model.pageCount == expect_page_count, (
                f"vagination pageCount is {pages_count}, expected {expect_page_count}"
            )

    @allure.title(TestsList.get_movies_list_positive_pagination_boundaries.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_positive_pagination_boundaries.parameters.arg_names,
        argvalues=TestsList.get_movies_list_positive_pagination_boundaries.parameters.arg_values,
    )
    def test_get_movies_list_positive_pagination_boundaries(
        self, su_session, page, page_size
    ):
        query = {"page": page, "pageSize": page_size}

        response_model = su_session.movies_api.get_movies_list(
            query=query, expected_status=HTTPStatus.OK
        )
        response_page_size = len(response_model.movies)

        with allure.step("Проверяем соответствие ответа ожидаемой пагинации"):
            assert query.get("pageSize") == response_page_size, (
                f"Запрос на размер страницы со списком фильмов был "
                f"{query.get('pageSize')}, но вернуло {response_page_size}"
            )

    @allure.title(TestsList.get_movies_list_check_sorting.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_movies_list_check_sorting.parameters.arg_names,
        argvalues=TestsList.get_movies_list_check_sorting.parameters.arg_values,
    )
    def test_get_movies_list_check_sorting(self, su_session, sorting, reversed_check):
        def check_date_times_sort(movies_list, reverse: bool = False):
            date_times = [item.createdAt for item in movies_list]
            with allure.step("Проверяем правильность сортировки по дате создания"):
                assert date_times == sorted(date_times, reverse=reverse), (
                    "Сортировка выполнена неверно"
                )

        response_model = su_session.movies_api.get_movies_list({"createdAt": sorting})

        check_date_times_sort(
            movies_list=response_model.movies, reverse=reversed_check
        )
