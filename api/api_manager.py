from requests import session

from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI


class ApiManager:
    def __init__(self, session, api_url, auth_url, headers):
        self.auth_api = AuthAPI(session=session, base_url=auth_url, headers=headers)
        self.movies_api = MoviesAPI(session=session, base_url=api_url, headers=headers)