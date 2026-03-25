from tools.dict_compare_similar_fields import dict_compare_similar_fields

def test_create(create_movie, api_manager_su):
    movie_id = create_movie.get("id")
    response = api_manager_su.movies_api.get_movie(movie_id, expected_status=200)
    movie_json_get = response.json()
    # Сравнение содержимого
    dict_compare_similar_fields(create_movie, movie_json_get)