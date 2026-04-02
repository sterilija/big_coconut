import pytest

from tools.data_generator import DataGenerator
from http import HTTPStatus
from faker import Faker

fake = Faker()

class TestNegativeGet:

    @pytest.mark.xfail  ##TODO для разрабов: Починить ответ 500, который приходит вместо 404 (баг)
    def test_get_movie_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()

        api_manager_su.movies_api.get_movie(
            movie_id=movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )

    def test_get_movie_negative_boundary_ids(self, api_manager_su):
        api_manager_su.movies_api.get_movie(
            movie_id=0,
            expected_status=HTTPStatus.NOT_FOUND
        )

        api_manager_su.movies_api.get_movie(
            movie_id=-1,
            expected_status=HTTPStatus.NOT_FOUND
        )

        api_manager_su.movies_api.get_movie(
            movie_id=-500,
            expected_status=HTTPStatus.NOT_FOUND
        )

    @pytest.mark.xfail  ##TODO и тут 500
    def test_get_movie_string_id(self, api_manager_su, create_movie):
        api_manager_su.movies_api.get_movie(
            movie_id="spiderman",
            expected_status=HTTPStatus.NOT_FOUND
        )

    def test_get_movies_list_wrong_query_type(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(
            query={
                "lunch": "pizza",
                "pageSize": -1,
                "page": "Mozzarella",
                "minPrice": False,
                "locations": ["kompot", 123],
                "published": "yes",
                "genreId": DataGenerator.too_big_number()
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )

    def test_get_movies_list_wrong_pagination(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": 0,
                "page": 1
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )

        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": -1,
                "page": -1
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )

        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": fake.random_int(min=21),
                "page": fake.random_int(min=1, max=30)
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )

    def test_get_movies_list_wrong_price(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(query={
            "minPrice": fake.random_int(min=531, max=1000000),
            "maxPrice": fake.random_int(min=1, max=531)
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )

        api_manager_su.movies_api.get_movies_list(query={
            "maxPrice": 2147483649
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )

        api_manager_su.movies_api.get_movies_list(query={
            "minPrice": 0,
            "maxPrice": 0
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )

    @pytest.mark.xfail #TODO BUG: Нет реакции на поле locations
    def test_get_movies_list_wrong_locations(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(
            query={
            "locations": ["NYC", "BKK"]
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )