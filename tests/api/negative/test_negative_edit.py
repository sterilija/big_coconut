from tools.data_generator import DataGenerator

class TestNegativeEdit:

    def test_edit_non_exits(self, api_manager_su):
        film_id = DataGenerator.too_big_number()
        new_json = DataGenerator.new_movie()
        api_manager_su.movies_api.edit_movie(
            movie_id=film_id,
            new_data_json=new_json,
            expect_status=404
        )

    def test_edit_wrong_params(self, api_manager_su, create_movie):
        new_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
            "mr.penis": "friend" #лишние строки API игнорирует
        }
        movie_id = create_movie.get("id")
        api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expect_status=400
        )