import pytest
import requests
from constants import DEFAULT_HEADERS, API_URL, AUTH_URL, AUTH_SU_CREDENTIALS
from api.api_manager import ApiManager


@pytest.fixture(scope="session")
def session_new():
    session =  requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def api_manager(session_new):
    return ApiManager(
        session=session_new,
        headers=DEFAULT_HEADERS,
        api_url=API_URL,
        auth_url=AUTH_URL
    )

@pytest.fixture(scope="session")
def api_manager_su(session_new):
    api_manager = ApiManager(
        session=session_new,
        headers=DEFAULT_HEADERS,
        api_url=API_URL,
        auth_url=AUTH_URL
    )
    api_manager.auth_api.login_user({
        "email": "api1@gmail.com",
        "password": "asdqwe123Q",
    })
    return api_manager