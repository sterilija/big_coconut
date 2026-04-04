from models.model import CreateMovieDto, MovieResponse
from http import HTTPStatus
from tools.compare_dicts_by_keys import compare_dicts_by_keys

class TestPositiveCreate:

    def test_create_movie(self, create_movie, api_manager_su):
        movie_id = create_movie.response.get("id")

        response = api_manager_su.movies_api.get_movie(
            movie_id,
            expected_status=HTTPStatus.OK
        )
        movie_response = response.json()

        compare_dicts_by_keys(
            dict_original=create_movie.payload,
            dict_expected=movie_response,
            keys=CreateMovieDto.model_fields.keys(),
            exception_message="Данные в отправленных полях фильма не соответствуют данным из ответа при его создании"
        )

        compare_dicts_by_keys(
            dict_original=create_movie.response,
            dict_expected=movie_response,
            keys=MovieResponse.model_fields.keys(),
            exception_message="Данные в ответе после создания фильма не соответствуют данным при его получении"
        )
