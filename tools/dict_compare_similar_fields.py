from models.model import MovieResponse, CreateMovieDto


def dict_compare_similar_fields(
        payload: MovieResponse | CreateMovieDto,
        response_json: MovieResponse | CreateMovieDto
        ):
    for k, v in payload.items():
        assert response_json[k] == v, f'field "{k}" has different values in the comparing dicts'