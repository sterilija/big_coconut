from tools.compare_dicts_by_keys import compare_dicts_by_keys
from tools.data_generator import DataGenerator
from http import HTTPStatus
from models.model import CreateMovieDto

class TestNegativeEdit:

    def test_edit_movie_wrong_id(self, api_manager_su):
        expected_message = "Фильм не найден"
        fake_id = DataGenerator.too_big_number()
        new_json = DataGenerator.new_movie()

        response = api_manager_su.movies_api.edit_movie(
            movie_id=fake_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")
        assert response_message == expected_message,\
            "Неверное сообщение в ответе при редактировании несуществующего фильма"

    def test_edit_movie_wrong_params(self, api_manager_su, create_movie):
        expected_message = [
        "Поле name должно быть строкой",
        "location must be one of the following values: MSK, SPB",
        "Поле location должно быть строкой"
        ]
        new_json = {
            "name": [],
            "is_published": "cheese",
            "genre_id": False,
            "location": {"loc": "OG Loc"},
            "mr.penis": "friend" #TODO для аналитиков: задокументировать что лишние строки API игнорирует
        }
        movie_id = create_movie.response.get("id")

        response = api_manager_su.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message,\
            "Неправильное сообщение в ответе при неправильном изменении полей"

        response = api_manager_su.movies_api.get_movie(movie_id)

        compare_dicts_by_keys(
            negative=True,
            dict_original=new_json,
            dict_expected=response.json(),
            keys=list(new_json.keys()),
            exception_message=(
                "Неправильные поля при изменении фильма вызвали 400, но апдейт этих полей всё равно произошёл"
            )
        )

    def test_edit_movie_noauth(self, api_manager_noauth, create_movie):
        expected_message = "Unauthorized"
        movie_id = create_movie.response.get("id")
        new_json = DataGenerator.new_movie()

        response = api_manager_noauth.movies_api.edit_movie(
            movie_id=movie_id,
            new_data_json=new_json,
            expected_status=HTTPStatus.UNAUTHORIZED
        )
        response_message = response.json().get("message")

        assert response_message == expected_message,\
            "Неправильный ответ в сообщении при изменении полей без авторизации"

        response = api_manager_noauth.movies_api.get_movie(movie_id)

        compare_dicts_by_keys(
            negative=True,
            dict_original=new_json,
            dict_expected=response.json(),
            keys=CreateMovieDto.model_fields.keys(),
            exception_message=(
                "Неавторизованный пользователь смог изменить данные фильма"
            )
        )