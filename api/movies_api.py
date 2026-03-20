from requester.requester import CustomRequester
from models.model import CreateMovieDto, FindMoviesQuery
from api.constants import MOVIES_ENDPOINT

class MoviesAPI(CustomRequester):
    def __init__(self, session, base_url, headers):
        super().__init__(
            session=session,
            base_url=base_url,
            headers=headers
        )

    def create_movie(self, data_json: CreateMovieDto):
        return self.send_request(
            method="POST",
            expect_status=201,
            endpoint=MOVIES_ENDPOINT,
            data_json=data_json,
        )

    def get_movies_list(self, query: FindMoviesQuery):
        return self.send_request(
            method="GET",
            expect_status=200,
            endpoint=MOVIES_ENDPOINT,
            query=query
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            expect_status=expected_status,
            endpoint=f"{self.base_url}/{MOVIES_ENDPOINT}/{movie_id}",
        )

    def delete_movie(self, movie_id, expect_status=200):
        return self.send_request(
            method="DELETE",
            expect_status=expect_status,
            endpoint=f"{self.base_url}/{MOVIES_ENDPOINT}/{movie_id}",
        )

    def edit_movie(self, movie_id, new_data_json: CreateMovieDto):
        return self.send_request(
            method="PATCH",
            expect_status=200,
            endpoint=f"{self.base_url}/{MOVIES_ENDPOINT}/{movie_id}",
            data_json=new_data_json
        )