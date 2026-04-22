from http import HTTPStatus
from typing import Any

import allure
from requests import HTTPError
from requests import Session

from models.api.server_error_model import ErrorMessage
from models.api.user_model import (
    AuthPayload,
    AuthSuccessResponse,
    CreateUserDto,
    FindAllUsersResponse,
    UserResponse,
)
from requester.requester import CustomRequester


class UserAPI(CustomRequester):
    def __init__(self, session: Session, base_url: str, headers: dict[str, str]):
        super().__init__(session=session, base_url=base_url, headers=headers)
        self._login_endpoint = "login"
        self._register_endpoint = "register"

    def get_user(
        self,
        user_locator: str,
        query: dict[str, Any] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> UserResponse | FindAllUsersResponse | ErrorMessage | dict:
        step_message = "Получаем пользователя"
        success_model = UserResponse
        if user_locator == "":
            step_message = "Получаем список пользователей"
            success_model = FindAllUsersResponse

        with allure.step(step_message):
            allure.attach(
                str(user_locator),
                name="Локатор пользователя",
                attachment_type=allure.attachment_type.TEXT,
            )

            return self.send_request(
                method="GET",
                endpoint=f"user/{user_locator}",
                expected_status=expected_status,
                query=query,
                success_model=success_model,
            )

    def register_user(
        self,
        user_json: CreateUserDto,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> UserResponse | ErrorMessage:
        with allure.step("регистрируем пользователя"):
            return self.send_request(
                method="POST",
                endpoint=self._register_endpoint,
                data_json=user_json,
                expected_status=expected_status,
                success_model=UserResponse,
            )

    def login_user(
        self,
        login_json: AuthPayload | dict,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> AuthSuccessResponse | ErrorMessage:
        with allure.step("логиним пользователя"):
            response = self.send_request(
                method="POST",
                endpoint=self._login_endpoint,
                data_json=login_json,
                expected_status=expected_status,
                success_model=AuthSuccessResponse,
            )

        if not isinstance(response, AuthSuccessResponse):
            return response

        self._update_session_headers()
        access_token = response.accessToken

        if not access_token:
            raise HTTPError("Auth ручка не вернула токен")

        self._update_session_headers(Authorization=f"Bearer {access_token}")

        return response
