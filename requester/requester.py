import requests
import json
import os
import logging

from models.http_status_codes import HTTPStatusCodes


class CustomRequester:
    def __init__(self, session: requests.Session, headers: dict[str, str], base_url: str):
        self.session = session
        self.headers = headers
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self,
                     method,
                     endpoint,
                     headers=None,
                     expect_status=HTTPStatusCodes.Success,
                     data_json=None,
                     need_logging=True,
                     query=None
                     ):
        response = self.session.request(
            method=method,
            url=f"{self.base_url}/{endpoint}",
            json=data_json,
            headers=headers,
            params=query
        )
        assert response.status_code == expect_status,\
            f"Unexpected HTTP status code {response.status_code}, expected {expect_status}"
        if need_logging: self.log_request_and_response(response)
        return  response

    def log_request_and_response(self, response):
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
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
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def get_session(self):
        return self.session