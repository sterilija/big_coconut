import requests

from requester.requester import CustomRequester
from models.model import CreateMovieDto
from api.constants import MOVIES_ENDPOINT
from models.http_status_codes import HTTPStatusCodes
from models.model import FindMoviesQuery

class MoviesAPI(CustomRequester):
    def __init__(self, session: requests.Session, base_url: str, headers: dict[str, str]):
        super().__init__(
            session=session,
            base_url=base_url,
            headers=headers
        )

    def create_movie(self, data_json: CreateMovieDto, expect_status=HTTPStatusCodes.Created):
        return self.send_request(
            method="POST",
            expect_status=expect_status,
            endpoint=MOVIES_ENDPOINT,
            data_json=data_json,
        )

    def get_movies_list(self, query: FindMoviesQuery, expect_status=HTTPStatusCodes.Success):
        return self.send_request(
            method="GET",
            expect_status=expect_status,
            endpoint=MOVIES_ENDPOINT,
            query=query
        )

    def get_movie(self, movie_id: int, expected_status=HTTPStatusCodes.Success):
        return self.send_request(
            method="GET",
            expect_status=expected_status,
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
        )

    def delete_movie(self, movie_id: int, expect_status=HTTPStatusCodes.Success):
        return self.send_request(
            method="DELETE",
            expect_status=expect_status,
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
        )

    def edit_movie(self, movie_id: int, new_data_json: CreateMovieDto, expect_status=HTTPStatusCodes.Success):
        return self.send_request(
            method="PATCH",
            expect_status=expect_status,
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data_json=new_data_json
        )