from tools.data_generator import DataGenerator
from http import HTTPStatus

NOT_FOUND_MSG = "Фильм не найден"
NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG = "Неверный ответ при удалении не существующего фильма"

class TestNegativeDelete:

    def test_delete_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()

        response = api_manager_su.movies_api.delete_movie(
            movie_id=movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG

    def test_delete_same_id_twice(self, api_manager_su, create_movie):
        movie_id = create_movie.response.get("id")

        api_manager_su.movies_api.delete_movie(movie_id)
        response = api_manager_su.movies_api.delete_movie(
            movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_DELETION_EXCEPTION_MSG

        response = api_manager_su.movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG