from requests import Session

from requester.requester import CustomRequester
from models.model import CreateMovieDto
from http import HTTPStatus
from models.model import FindMoviesQuery

class MoviesAPI(CustomRequester):

    def __init__(self, session: Session, base_url: str, headers: dict[str, str]):
        super().__init__(
            session=session,
            base_url=base_url,
            headers=headers
        )
        self._movies_endpoint = 'movies'

    def create_movie(self, data_json: CreateMovieDto, expected_status=HTTPStatus.CREATED):
        return self.send_request(
            method="POST",
            expected_status=expected_status,
            endpoint=self._movies_endpoint,
            data_json=data_json,
        )

    def get_movies_list(self, query: FindMoviesQuery, expected_status=HTTPStatus.OK):
        return self.send_request(
            method="GET",
            expected_status=expected_status,
            endpoint=self._movies_endpoint,
            query=query
        )

    def get_movie(self, movie_id: int, expected_status=HTTPStatus.OK):
        return self.send_request(
            method="GET",
            expected_status=expected_status,
            endpoint=f"{self._movies_endpoint}/{movie_id}",
        )

    def delete_movie(self, movie_id: int, expected_status=HTTPStatus.OK):
        return self.send_request(
            method="DELETE",
            expected_status=expected_status,
            endpoint=f"{self._movies_endpoint}/{movie_id}",
        )

    def edit_movie(self, movie_id: int, new_data_json: CreateMovieDto, expected_status=HTTPStatus.OK):
        return self.send_request(
            method="PATCH",
            expected_status=expected_status,
            endpoint=f"{self._movies_endpoint}/{movie_id}",
            data_json=new_data_json
        )