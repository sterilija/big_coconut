from typing import Any

import pytest
from http import HTTPStatus

from tools.data_generator import DataGenerator

query_list_movies_desc = {"createdAt": "desc"}

class TestNegativeCreate:

    def test_create_movie_empty_body(self, api_manager_su):
        expected_message = [
        "name should not be empty",
        "Поле name должно быть строкой",
        "Поле price должно быть числом",
        "Поле description должно быть строкой",
        "Поле location должно быть одним из: MSK, SPB",
        "Поле location должно быть строкой",
        "Поле published должно быть булевым значением",
        "Поле genreId должно быть числом"
        ]

        response = api_manager_su.movies_api.create_movie(
            data_json={},
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message, "Ответ при создании пустотелого фильма не соответствует ожидаемому"

    def test_create_movie_name_already_exists(self, create_movie, api_manager_su):
        expected_message = "Фильм с таким названием уже существует"
        movie_name = create_movie.response.get('name')
        new_movie_json = DataGenerator.new_movie()
        new_movie_json["name"] = movie_name

        response = api_manager_su.movies_api.create_movie(
            data_json=new_movie_json,
            expected_status=HTTPStatus.CONFLICT
        )
        response_message = response.json().get("message")

        assert response_message == expected_message

    def test_create_movie_wrong_field_type(self, api_manager_su):
        new_movie_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
        }

        api_manager_su.movies_api.create_movie(
            new_movie_json,
            expected_status=HTTPStatus.BAD_REQUEST
        )

    def test_create_movie_noauth(self, api_manager_noauth):
        expected_message = "Unauthorized"
        new_movie = DataGenerator.new_movie()

        response = api_manager_noauth.movies_api.create_movie(
            data_json=new_movie,
            expected_status=HTTPStatus.UNAUTHORIZED
        )
        response_message = response.json().get("message")

        assert expected_message == response_message

    def test_create_movie_missing_name(self, api_manager_su):
        expected_message = [
        "name should not be empty",
        "Поле name должно быть строкой"
        ]
        new_movie = DataGenerator.new_movie()
        new_movie.pop("name")

        response = api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert expected_message == response_message

    @pytest.mark.xfail #TODO разрабам: Сделать запрет или экранирование XSS-атак
    def test_create_movie_attack_xss(self, api_manager_su):
        new_movie = DataGenerator.new_movie(
            name="<script>alert(1)</script>",
        )

        api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expected_status=HTTPStatus.BAD_REQUEST
        )

    @pytest.mark.xfail # TODO разрабам: Сделать запрет или экранирование SQL_injection-атак
    def test_create_movie_attack_sqli(self, api_manager_su):
        new_movie = DataGenerator.new_movie(
            name= "' OR 1=1",
        )

        api_manager_su.movies_api.create_movie(
            data_json=new_movie,
            expected_status=HTTPStatus.BAD_REQUEST
        )
