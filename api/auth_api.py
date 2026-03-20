from api.movies_api import MoviesAPI
from api.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from requester.requester import CustomRequester


class AuthAPI(CustomRequester):
    def __init__(self, session, base_url, headers):
        super().__init__(session=session, base_url=base_url, headers=headers)

    def register_user(self, user_jsom, expect_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data_json=user_jsom,
            expect_status=expect_status
        )

    def login_user(self, login_json, expect_status=200):
        response = self.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data_json=login_json,
            expect_status=expect_status
        )
        self._update_session_headers()