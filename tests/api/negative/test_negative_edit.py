from tools.data_generator import DataGenerator
from models.http_status_codes import HTTPStatusCodes
class TestNegativeEdit:

    def test_edit_wrong_id(self, api_manager_su):
        fake_id = DataGenerator.too_big_number()
        new_json = DataGenerator.new_movie()
        api_manager_su.movies_api.edit_movie(
            movie_id=fake_id,
            new_data_json=new_json,
            expect_status=HTTPStatusCodes.NotFound
        )

    def test_edit_wrong_params(self, api_manager_su, create_movie):
        new_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
            "mr.penis": "friend" #TODO задокументировать что лишние строки API игнорирует
        }
        movie_id = create_movie.get("id")
        api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expect_status=HTTPStatusCodes.WrongData
        )

    def test_edit_noauth(self, api_manager_noauth, create_movie):
        movie_id = create_movie.get("id")
        api_manager_noauth.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=DataGenerator.new_movie(),
            expect_status=HTTPStatusCodes.Unauthorized
        )