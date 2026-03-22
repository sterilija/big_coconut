import pytest

from tools.data_generator import DataGenerator

class TestNegativeGet:

    @pytest.mark.xfail ##TODO для разрабов: Починить ответ 500, который приходит вместо 404 (баг)
    def test_get_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()
        api_manager_su.movies_api.get_movie(
            movie_id=movie_id,
            expected_status=404
        )

    def test_get_corner_ids(self, api_manager_su):
        api_manager_su.movies_api.get_movie(
            movie_id=0,
            expected_status=404
        )
        api_manager_su.movies_api.get_movie(
            movie_id=-1,
            expected_status=404
        )
        api_manager_su.movies_api.get_movie(
            movie_id=-500,
            expected_status=404
        )

    @pytest.mark.xfail  ##TODO и тут 500
    def test_get_string_id(self, api_manager_su, create_movie):
        api_manager_su.movies_api.get_movie(
            movie_id="spiderman",
            expected_status=404
        )

    def test_get_list_movies_wrong_query(self, api_manager_su):
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
            expect_status=400
        )

    def test_get_list_movies_query_corner_nums(self, api_manager_su):
        #Сначала нули
        api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": 0,
                "page": 0,
                "minPrice": 0,
                "maxPrice": 0,
            },
            expect_status=400
        )
        #