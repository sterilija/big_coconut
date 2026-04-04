from http import HTTPStatus

class TestPositiveDelete:

    def test_delete_movie(self, create_movie, api_manager_su):
        movie_id = create_movie.response.get("id")

        api_manager_su.movies_api.delete_movie(movie_id)

        api_manager_su.movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)