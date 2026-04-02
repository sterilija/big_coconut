from models.model import CreateMovieDto, MovieResponse
from tools.compare_dicts_by_keys import compare_dicts_by_keys
from tools.data_generator import DataGenerator
from faker import Faker

fake = Faker()

NEW_DATA_TO_GET_MISMATCH_MSG = "Полученный фильм не соответствует сделанным изменениям"
NEW_DATA_TO_RESPONSE_MISMATCH_MSG = "Ответ при изменении фильма не соответствует сделанным изменениям"

class TestPositiveUpdate:

    def test_update_movie_full(self, create_movie, api_manager_su):
        movie_id = create_movie.response.get("id")
        patch_payload = DataGenerator.new_movie()

        patch_response = api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=patch_payload,
        ).json()
        get_response = api_manager_su.movies_api.get_movie(movie_id).json()

        compare_dicts_by_keys(
            patch_payload,
            patch_response,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_RESPONSE_MISMATCH_MSG
        )
        compare_dicts_by_keys(
            patch_payload,
            get_response,
            CreateMovieDto.model_fields.keys(),
            NEW_DATA_TO_GET_MISMATCH_MSG
        )

    def test_update_movie_partial(self, create_movie, api_manager_su):
        movie_id = create_movie.response.get("id")
        patch_payload = {
            "name": fake.sentence(nb_words=4, variable_nb_words=True),
            "description": fake.text(max_nb_chars=100)
        }

        patch_response = api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=patch_payload,
        ).json()
        get_response = api_manager_su.movies_api.get_movie(movie_id).json()

        compare_dicts_by_keys(
            patch_payload,
            patch_response,
            list(patch_payload.keys()),
            NEW_DATA_TO_RESPONSE_MISMATCH_MSG
        )
        compare_dicts_by_keys(
            patch_payload,
            get_response,
            list(patch_payload.keys()),
            NEW_DATA_TO_GET_MISMATCH_MSG
        )