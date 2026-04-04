from tools.data_generator import DataGenerator
from http import HTTPStatus

class TestNegativeDelete:

    def test_delete_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()

        api_manager_su.movies_api.delete_movie(
            movie_id=movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )

    def test_delete_same_id_twice(self, api_manager_su, create_movie):
        movie_id = create_movie.response.get("id")

        api_manager_su.movies_api.delete_movie(movie_id)
        api_manager_su.movies_api.delete_movie(
            movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )