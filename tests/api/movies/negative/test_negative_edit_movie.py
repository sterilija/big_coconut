from tools.data_generator import DataGenerator
from http import HTTPStatus

class TestNegativeEdit:

    def test_edit_movie_wrong_id(self, api_manager_su):
        fake_id = DataGenerator.too_big_number()
        new_json = DataGenerator.new_movie()

        api_manager_su.movies_api.edit_movie(
            movie_id=fake_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.NOT_FOUND
        )

    def test_edit_movie_wrong_params(self, api_manager_su, create_movie):
        new_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
            "mr.penis": "friend" #TODO для аналитиков: задокументировать что лишние строки API игнорирует
        }
        movie_id = create_movie.response.get("id")

        api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.BAD_REQUEST
        )

    def test_edit_movie_noauth(self, api_manager_noauth, create_movie):
        movie_id = create_movie.response.get("id")

        api_manager_noauth.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=DataGenerator.new_movie(),
            expected_status=HTTPStatus.UNAUTHORIZED
        )