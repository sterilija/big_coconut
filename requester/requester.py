from typing import Any, TypeVar

from requests import Response
from pydantic import BaseModel
from requests import Session
import json
import os
import logging
import allure

from http import HTTPStatus
from constants.colors import RED, GREEN, RESET
from models.api.server_error_model import ErrorMessage

T = TypeVar("T", bound=BaseModel)


def is_success_status(status: HTTPStatus) -> bool:
    return HTTPStatus.OK <= status < HTTPStatus.MULTIPLE_CHOICES


class CustomRequester:
    def __init__(self, session: Session, headers: dict[str, str], base_url: str):
        self.session = session
        self.headers = headers
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, Any] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
        data_json: dict[str, Any] = None,
        need_logging: bool = True,
        query: dict[str, Any] = None,
        success_model: type[T] | None = None,
        error_model: type[BaseModel] | None = ErrorMessage,
    ) -> Response | T | ErrorMessage | dict | None:
        if isinstance(data_json, BaseModel):
            data_json = json.loads(data_json.model_dump_json(exclude_unset=True))

        if isinstance(query, BaseModel):
            query = json.loads(query.model_dump_json(exclude_unset=True))

        with allure.step("Запрос на сервер:"):
            if headers is not None:
                allure.attach(
                    json.dumps(headers, indent=4, ensure_ascii=False),
                    name="Доп. заголовки",
                    attachment_type=allure.attachment_type.JSON,
                )

            allure.attach(
                json.dumps(self.headers, indent=4, ensure_ascii=False),
                name="Заголовки",
                attachment_type=allure.attachment_type.JSON,
            )

            allure.attach(
                endpoint,
                name="Ручка",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                json.dumps(query, indent=4, ensure_ascii=False),
                name="query-параметры",
                attachment_type=allure.attachment_type.JSON,
            )

            allure.attach(
                method,
                name="Метод",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                str(expected_status),
                name="Ожидаемый статус ответа",
                attachment_type=allure.attachment_type.TEXT,
            )

            if data_json is not None:
                allure.attach(
                    json.dumps(data_json, indent=4, ensure_ascii=False),
                    name="Тело запроса",
                    attachment_type=allure.attachment_type.JSON,
                )

            response = self.session.request(
                method=method,
                url=f"{self.base_url}/{endpoint}",
                json=data_json,
                headers=headers,
                params=query,
            )

        with allure.step("Получен ответ:"):
            allure.attach(
                str(response.status_code),
                name="Статус ответа",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                json.dumps(response.json(), indent=4, ensure_ascii=False),
                name="Тело ответа",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка соответствия ожидаемому статусу..."):
            assert response.status_code == expected_status, (
                f"Unexpected HTTP status code {response.status_code}, expected {expected_status}"
            )

        if need_logging:
            self.log_request_and_response(response)

        if success_model is None and error_model is None:
            return response

        return self._parse_response(
            response=response,
            expected_status=expected_status,
            success_model=success_model,
            error_model=error_model,
        )

    def _parse_response(
        self,
        response: Response,
        expected_status: HTTPStatus,
        success_model: type[T] | None,
        error_model: type[BaseModel] | None,
    ) -> T | ErrorMessage | dict | None:
        body = response.json() if response.content else {}

        if is_success_status(expected_status):
            if success_model is None:
                return body if body else None
            if not body:
                return body
            return success_model.model_validate(body)

        error_cls = error_model or ErrorMessage
        return error_cls.model_validate(body)

    def log_request_and_response(self, response: Response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join(
                [f"-H '{header}: {value}'" for header, value in request.headers.items()]
            )
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
                body = f"-d '{body}' \n" if body != "{}" else ""

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(
                    json.loads(response.text), indent=4, ensure_ascii=False
                )
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response.status_code}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response.status_code}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")

    def _update_session_headers(self, **kwargs):
        with allure.step("Обновляем заголовки"):
            allure.attach(
                json.dumps(self.headers, indent=4, ensure_ascii=False),
                name="Было",
                attachment_type=allure.attachment_type.JSON,
            )

            allure.attach(
                json.dumps(kwargs, indent=4, ensure_ascii=False),
                name="Изменили/добавили",
                attachment_type=allure.attachment_type.JSON,
            )

            self.headers.update(kwargs)
            self.session.headers.update(self.headers)

            allure.attach(
                json.dumps(self.headers, indent=4, ensure_ascii=False),
                name="Стало",
                attachment_type=allure.attachment_type.JSON,
            )

    def get_session(self):
        return self.session
