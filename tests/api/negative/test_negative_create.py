import pytest
from models.http_status_codes import HTTPStatusCodes
from tools.data_generator import DataGenerator

class TestNegativeEdit:

    def test_create_empty(self, api_manager_su):
        api_manager_su.movies_api.create_movie(
            data_json={},
            expect_status=HTTPStatusCodes.WrongData
        )

    def test_create_name_exists(self, create_movie, api_manager_su):
        movie_name = create_movie.get('name')
        new_movie_json = DataGenerator.new_movie()
        new_movie_json["name"] = movie_name
        api_manager_su.movies_api.create_movie(
            new_movie_json,
            expect_status=HTTPStatusCodes.Conflict
        )

    def test_create_wrong_type(self, api_manager_su):
        new_movie_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
        }
        api_manager_su.movies_api.create_movie(
            new_movie_json,
            expect_status=HTTPStatusCodes.WrongData
        )

    def test_create_noauth(self, api_manager_noauth):
        new_movie = DataGenerator.new_movie()
        api_manager_noauth.movies_api.create_movie(
            data_json=new_movie,
            expect_status=HTTPStatusCodes.Unauthorized
        )

    def test_create_missing_name(self, api_manager_su):
        new_movie = DataGenerator.new_movie()
        new_movie.pop("name")
        api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expect_status=HTTPStatusCodes.WrongData
        )

    @pytest.mark.xfail #TODO разрабам: Сделать запрет или экранирование XSS-атак
    def test_create_xss(self, api_manager_su):
        new_movie = DataGenerator.new_movie(
            name="<script>alert(1)</script>",
        )
        api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expect_status=HTTPStatusCodes.WrongData
        )

    @pytest.mark.xfail # TODO разрабам: Сделать запрет или экранирование SQL_injection-атак
    def test_create_sqli(self, api_manager_su):
        new_movie = DataGenerator.new_movie(
            name= "' OR 1=1",
        )
        api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expect_status=HTTPStatusCodes.WrongData
        )
