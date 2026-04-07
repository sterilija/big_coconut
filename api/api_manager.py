from requests import Session
from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI


class ApiManager:

    def __init__(self, session: Session, api_url: str, auth_url: str, headers: dict[str, str]):
        self.auth_api = AuthAPI(session=session, base_url=auth_url, headers=headers)
        self.movies_api = MoviesAPI(session=session, base_url=api_url, headers=headers)