import pytest

from tools.data_generator import DataGenerator
from http import HTTPStatus
from faker import Faker

fake = Faker()

NOT_FOUND_MSG = "Фильм не найден"
WRONG_DATA_MSG = "Некорректные данные"
NON_EXISTING_MOVIE_GET_EXCEPTION_MSG = "Неверное сообщение в ответе при получении не существующего фильма"

class TestNegativeGet:

    @pytest.mark.xfail  ##TODO для разрабов: Починить ответ 500, который приходит вместо 404 (баг)
    def test_get_movie_wrong_id(self, api_manager_su):
        movie_id = DataGenerator.too_big_number()

        response = api_manager_su.movies_api.get_movie(
            movie_id=movie_id,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_GET_EXCEPTION_MSG

    def test_get_movie_negative_boundary_ids(self, api_manager_su):
        response = api_manager_su.movies_api.get_movie(
            movie_id=0,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_GET_EXCEPTION_MSG

        response = api_manager_su.movies_api.get_movie(
            movie_id=-1,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_GET_EXCEPTION_MSG

        response = api_manager_su.movies_api.get_movie(
            movie_id=-500,
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_GET_EXCEPTION_MSG

    @pytest.mark.xfail  ##TODO и тут 500
    def test_get_movie_string_id(self, api_manager_su, create_movie):
        response = api_manager_su.movies_api.get_movie(
            movie_id="spiderman",
            expected_status=HTTPStatus.NOT_FOUND
        )
        response_message = response.json().get("message")

        assert response_message == NOT_FOUND_MSG, NON_EXISTING_MOVIE_GET_EXCEPTION_MSG

    def test_get_movies_list_wrong_query_type(self, api_manager_su):
        expected_message = [
            "Поле pageSize имеет минимальную величину 1",
            "Поле page имеет минимальную величину 1",
            "Поле page должно быть числом",
            "Поле minPrice имеет минимальную величину 1",
            "Поле minPrice должно быть числом",
            "Поле genreId должно быть числом"
        ]

        response = api_manager_su.movies_api.get_movies_list(
            query={
                "lunch": "pizza",
                "pageSize": -1,
                "page": "Mozzarella",
                "minPrice": False,
                "locations": ["kompot", 123],
                "published": "yes",
                "genreId": DataGenerator.too_big_number()
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message, \
            "Неверное сообщение в ответе при попытке получить фильм с неправильными query-параметрами"

    def test_get_movies_list_wrong_pagination(self, api_manager_su):
        expected_message = [
            "Поле pageSize имеет минимальную величину 1"
        ]

        response = api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": 0,
                "page": 1
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message,\
            "Неверное сообщение в ответе при попытке получить список фильмов с PageSize < 1"

        expected_message = [
            "Поле pageSize имеет минимальную величину 1",
            "Поле page имеет минимальную величину 1"
        ]

        response = api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": -1,
                "page": -1
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message, \
            "Неверное сообщение в ответе при попытке получить список фильмов с pageSize < 1 и page < 1"

        expected_message = [
            "Поле pageSize имеет максимальную величину 20"
        ]

        response = api_manager_su.movies_api.get_movies_list(
            query={
                "pageSize": fake.random_int(min=21),
                "page": fake.random_int(min=1, max=30)
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message, \
            "Неверное сообщение в ответе при попытке получить список фильмов с pageSize > 20"

    def test_get_movies_list_wrong_price(self, api_manager_su):
        expected_message = "minPrice must be less than maxPrice"

        response = api_manager_su.movies_api.get_movies_list(query={
            "minPrice": fake.random_int(min=531, max=1000000),
            "maxPrice": fake.random_int(min=1, max=531)
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message,\
            "Неверное сообщение в ответе при попытке получить список фильмов с minPrice > maxPrice"


        expected_message = WRONG_DATA_MSG

        response = api_manager_su.movies_api.get_movies_list(query={
            "maxPrice": 2147483649
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == expected_message, \
            "Неверное сообщение в ответе при попытке получить список фильмов со слишком большой ценой"

        expected_message = [
            "Поле minPrice имеет минимальную величину 1"
        ]

        response = api_manager_su.movies_api.get_movies_list(query={
            "minPrice": 0,
            "maxPrice": 0
        },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert expected_message == response_message, \
            "Неверное сообщение в ответе при попытке получить список фильмов с minPrice < 1"

    @pytest.mark.xfail #TODO BUG: Нет реакции на поле locations
    def test_get_movies_list_wrong_locations(self, api_manager_su):
        response = api_manager_su.movies_api.get_movies_list(
            query={
            "locations": ["NYC", "BKK"]
            },
            expected_status=HTTPStatus.BAD_REQUEST
        )
        response_message = response.json().get("message")

        assert response_message == WRONG_DATA_MSG,\
            "Неверное сообщение при попытке получить список фильмов с неправильными городами"