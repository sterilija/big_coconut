from requests import Session
from modules.api.user_api import UserAPI
from modules.api.movies_api import MoviesAPI


class ApiManager:
    def __init__(
        self, session: Session, api_url: str, auth_url: str, headers: dict[str, str]
    ):
        self.session = session
        self.user_api = UserAPI(session=session, base_url=auth_url, headers=headers)
        self.movies_api = MoviesAPI(session=session, base_url=api_url, headers=headers)

    def close_session(self):
        self.session.close()
