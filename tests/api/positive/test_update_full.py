from tools.dict_comparison_partial import dict_comparison_partial
from tools.data_generator import DataGenerator

def test_update_full(create_movie, api_manager_su):
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
    dict_comparison_partial(new_movie_json, response_movie)
    dict_comparison_partial(new_movie_json, get_movie)