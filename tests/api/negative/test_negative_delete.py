from tools.data_generator import DataGenerator

class TestNegativeDelete:

    def test_delete_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()
        api_manager_su.movies_api.delete_movie(
            movie_id=movie_id,
            expect_status=404
        )