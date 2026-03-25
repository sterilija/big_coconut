from tools.dict_compare_similar_fields import dict_compare_similar_fields
from tools.pick_random_fields import pick_random_fields
from tools.data_generator import DataGenerator


class TestPositiveUpdate:

    def test_update_full(self, create_movie, api_manager_su):
        movie_id = create_movie.get("id")
        new_movie_json = DataGenerator.new_movie()
        response = api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_movie_json,
        )
        response_movie = response.json()
        # Проверка изменений
        response = api_manager_su.movies_api.get_movie(movie_id)
        get_movie = response.json()
        dict_compare_similar_fields(new_movie_json, response_movie)
        dict_compare_similar_fields(new_movie_json, get_movie)

    def test_update_patrial(self, create_movie, api_manager_su):
        movie_id = create_movie.get("id")
        new_json_partial = DataGenerator.new_movie()
        new_json_partial = pick_random_fields(new_json_partial)
        response = api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json_partial,
        )
        film_updated = response.json()
        dict_compare_similar_fields(new_json_partial, film_updated)
