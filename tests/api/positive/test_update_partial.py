from tools.dict_comparison_partial import dict_comparison_partial
from tools.data_generator import DataGenerator
from tools.pick_random_fields import pick_random_fields

def test_update_patrial(create_movie, api_manager_su):
    movie_id = create_movie.get("id")
    new_json_partial = DataGenerator.new_movie()
    new_json_partial = pick_random_fields(new_json_partial)
    response = api_manager_su.movies_api.edit_movie(
        movie_id=movie_id,
        new_data_json=new_json_partial,
    )
    film_updated = response.json()
    dict_comparison_partial(new_json_partial, film_updated)
