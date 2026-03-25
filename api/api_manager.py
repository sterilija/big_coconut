import requests
from requests import session

from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI


class ApiManager:
    def __init__(self, http_session: requests.Session, api_url: str, auth_url: str, headers: dict[str, str]):
        self.auth_api = AuthAPI(session=http_session, base_url=auth_url, headers=headers)
        self.movies_api = MoviesAPI(session=http_session, base_url=api_url, headers=headers)