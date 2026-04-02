from requests import HTTPError
from http import HTTPStatus
from requester.requester import CustomRequester
from models.model import AuthPayload, UserRegisterData


class AuthAPI(CustomRequester):

    def __init__(self, session, base_url, headers):
        super().__init__(session=session, base_url=base_url, headers=headers)
        self._login_endpoint = "login"
        self._register_endpoint = 'register'

    def register_user(self, user_json: UserRegisterData, expected_status=HTTPStatus.CREATED):
        return self.send_request(
            method="POST",
            endpoint=self._register_endpoint,
            data_json=user_json,
            expected_status=expected_status
        )

    def login_user(self, login_json: AuthPayload, expected_status=HTTPStatus.OK):
        response = self.send_request(
            method='POST',
            endpoint=self._login_endpoint,
            data_json=login_json,
            expected_status=expected_status
        )
        self._update_session_headers()
        access_token = response.json().get('accessToken')

        if not access_token:
            raise HTTPError("Auth ручка не вернула токен")

        self._update_session_headers(Authorization=f"Bearer {access_token}")

        return response