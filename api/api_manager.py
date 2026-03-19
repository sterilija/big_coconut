from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI


class ApiManager:
    def __init__(self, session, base_url, headers):
        self.auth_api = AuthAPI(session=session, base_url=base_url, headers=headers)
        self.movies_api = MoviesAPI(session=session, base_url=base_url, headers=headers)