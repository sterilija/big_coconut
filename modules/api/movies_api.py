from http import HTTPStatus

import allure
from requests import Session

from models.api.movies_model import (
    CreateMovieDto,
    EditMovieDto,
    FindAllMoviesResponse,
    FindMoviesQuery,
    MovieResponse,
)
from models.api.server_error_model import ErrorMessage
from requester.requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session: Session, base_url: str, headers: dict[str, str]):
        super().__init__(session=session, base_url=base_url, headers=headers)
        self._movies_endpoint = "movies"

    def create_movie(
        self,
        data_json: CreateMovieDto | dict,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> MovieResponse | ErrorMessage:
        with allure.step("Создаём фильм"):
            return self.send_request(
                method="POST",
                expected_status=expected_status,
                endpoint=self._movies_endpoint,
                data_json=data_json,
                success_model=MovieResponse,
            )

    def get_movies_list(
        self,
        query: FindMoviesQuery | dict,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> FindAllMoviesResponse | ErrorMessage:
        with allure.step("Получаем список фильмов"):
            return self.send_request(
                method="GET",
                expected_status=expected_status,
                endpoint=self._movies_endpoint,
                query=query,
                success_model=FindAllMoviesResponse,
            )

    def get_movie(
        self,
        movie_id: int | str,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> MovieResponse | ErrorMessage:
        with allure.step("Получаем фильм"):
            return self.send_request(
                method="GET",
                expected_status=expected_status,
                endpoint=f"{self._movies_endpoint}/{movie_id}",
                success_model=MovieResponse,
            )

    def delete_movie(
        self,
        movie_id: int,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> None | ErrorMessage:
        with allure.step("Удаляем фильм"):
            return self.send_request(
                method="DELETE",
                expected_status=expected_status,
                endpoint=f"{self._movies_endpoint}/{movie_id}",
            )

    def edit_movie(
        self,
        movie_id: int,
        new_data_json: CreateMovieDto | EditMovieDto | dict,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> MovieResponse | ErrorMessage:
        with allure.step("Редактируем фильм"):
            return self.send_request(
                method="PATCH",
                expected_status=expected_status,
                endpoint=f"{self._movies_endpoint}/{movie_id}",
                data_json=new_data_json,
                success_model=MovieResponse,
            )
