from http import HTTPStatus

class TestPositiveDelete:

    def test_delete_movie(self, create_movie, api_manager_su):
        expected_message = "Фильм не найден"
        movie_id = create_movie.response.get("id")

        api_manager_su.movies_api.delete_movie(movie_id)

        response = api_manager_su.movies_api.get_movie(
            movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == expected_message,\
            "После удаления фильма, нет сообщения в ответе о том что он не найден"