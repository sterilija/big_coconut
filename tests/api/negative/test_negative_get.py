import pytest

from tools.data_generator import DataGenerator
from models.http_status_codes import HTTPStatusCodes

class TestNegativeGet:

    @pytest.mark.xfail  ##TODO для разрабов: Починить ответ 500, который приходит вместо 404 (баг)
    def test_get_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()
        api_manager_su.movies_api.get_movie(
            movie_id=movie_id,
            expected_status=HTTPStatusCodes.NotFound
        )

    def test_get_negative_boundary_ids(self, api_manager_su):
        api_manager_su.movies_api.get_movie(
            movie_id=0,
            expected_status=HTTPStatusCodes.NotFound
        )
        api_manager_su.movies_api.get_movie(
            movie_id=-1,
            expected_status=HTTPStatusCodes.NotFound
        )
        api_manager_su.movies_api.get_movie(
            movie_id=-500,
            expected_status=HTTPStatusCodes.NotFound
        )

    @pytest.mark.xfail  ##TODO и тут 500
    def test_get_string_id(self, api_manager_su, create_movie):
        api_manager_su.movies_api.get_movie(
            movie_id="spiderman",
            expected_status=HTTPStatusCodes.NotFound
        )

    def test_get_list_wrong_query_type(self, api_manager_su):
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
            expect_status=HTTPStatusCodes.WrongData
        )

    def test_get_list_wrong_pagination(self, api_manager_su, faker_fxtr):
        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": 0,
                "page": 1
            },
            expect_status=HTTPStatusCodes.WrongData
        )

        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": -1,
                "page": -1
            },
            expect_status=HTTPStatusCodes.WrongData
        )

        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": faker_fxtr.random_int(min=21),
                "page": faker_fxtr.random_int(min=1, max=30)
            },
            expect_status=HTTPStatusCodes.WrongData
        )

    def test_get_list_wrong_price(self, api_manager_su, faker_fxtr):
        api_manager_su.movies_api.get_movies_list(query={
            "minPrice": faker_fxtr.random_int(min=531, max=1000000),
            "maxPrice": faker_fxtr.random_int(min=1, max=531)
        },
            expect_status=HTTPStatusCodes.WrongData
        )

        api_manager_su.movies_api.get_movies_list(query={
            "maxPrice": 2147483649
        },
            expect_status=HTTPStatusCodes.WrongData
        )

        api_manager_su.movies_api.get_movies_list(query={
            "minPrice": 0,
            "maxPrice": 0
        },
            expect_status=HTTPStatusCodes.WrongData
        )
    @pytest.mark.xfail #TODO BUG: Нет реакции на поле locations
    def test_get_list_wrong_locations(self, api_manager_su, faker_fxtr):
        api_manager_su.movies_api.get_movies_list(query={
            "locations": ["NYC", "BKK"]
        },
            expect_status=HTTPStatusCodes.WrongData
        )