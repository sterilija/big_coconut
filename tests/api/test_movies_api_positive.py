import requests

from constants import AUTH_SU_CREDENTIALS
from tools.data_generator import DataGenerator

class TestMoviesAPI:

    def test_create(self, api_manager_su):
        movie_json = DataGenerator.new_movie().model_dump(mode="json")
        response = api_manager_su.movies_api.create_movie(movie_json)
        movie_id = response.json().get("id")
        api_manager_su.movies_api.get_movie(movie_id, expected_status=404)