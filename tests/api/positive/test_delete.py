def test_delete(self, create_movie, api_manager_su):
    movie_id = create_movie.get("id")
    api_manager_su.movies_api.delete_movie(movie_id)
    # Проверка отсутствия
    api_manager_su.movies_api.get_movie(movie_id, expected_status=404)