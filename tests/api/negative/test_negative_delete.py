from tools.data_generator import DataGenerator
from models.http_status_codes import HTTPStatusCodes
class TestNegativeDelete:

    def test_delete_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()
        api_manager_su.movies_api.delete_movie(
            movie_id=movie_id,
            expect_status=HTTPStatusCodes.NotFound
        )

    def test_delete_twice(self, api_manager_su, create_movie):
        movie_id = create_movie.get("id")
        api_manager_su.movies_api.delete_movie(movie_id)
        api_manager_su.movies_api.delete_movie(
            movie_id,
            expect_status=HTTPStatusCodes.NotFound
        )