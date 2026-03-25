from tools.dict_comparison_partial import dict_comparison_partial

def test_create(create_movie, api_manager_su):
    movie_id = create_movie.get("id")
    response = api_manager_su.movies_api.get_movie(movie_id, expected_status=200)
    movie_json_get = response.json()
    # Сравнение содержимого
    dict_comparison_partial(create_movie, movie_json_get)