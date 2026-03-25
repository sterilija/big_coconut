import requests
from models.http_status_codes import HTTPStatusCodes
from api.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from requester.requester import CustomRequester
from models.model import AuthPayload, UserRegisterData


class AuthAPI(CustomRequester):
    def __init__(self, session, base_url, headers):
        super().__init__(session=session, base_url=base_url, headers=headers)

    def register_user(self, user_json: UserRegisterData, expect_status=HTTPStatusCodes.Created):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data_json=user_json,
            expect_status=expect_status
        )

    def login_user(self, login_json: AuthPayload, expect_status=HTTPStatusCodes.Success):
        response = self.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data_json=login_json,
            expect_status=expect_status
        )
        self._update_session_headers()
        access_token = response.json().get('accessToken')
        if access_token:
            self._update_session_headers(Authorization=f"Bearer {access_token}")
        else: raise requests.HTTPError("Auth ручка не вернула токен")
        return response