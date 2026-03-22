from tools.data_generator import DataGenerator

class TestNegativeEdit:

    def test_create_empty(self, api_manager_su):
        api_manager_su.movies_api.create_movie({}, expect_status=400)

    def test_create_name_exists(self, create_movie, api_manager_su):
        movie_name = create_movie.get('name')
        new_movie_json = DataGenerator.new_movie()
        new_movie_json["name"] = movie_name
        api_manager_su.movies_api.create_movie(new_movie_json, expect_status=409)

    def test_create_wrong_type(self, api_manager_su):
        new_movie_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
        }
        api_manager_su.movies_api.create_movie(new_movie_json, expect_status=400)
