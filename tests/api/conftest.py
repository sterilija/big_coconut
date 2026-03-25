import pytest
import requests
from api.api_manager import ApiManager
from constants import DEFAULT_HEADERS, API_URL, AUTH_URL
from tools.data_generator import DataGenerator
from faker import Faker


@pytest.fixture(scope="session")
def api_manager_su():
    session = requests.Session()
    api_manager = ApiManager(
        http_session=session,
        headers=DEFAULT_HEADERS,
        api_url=API_URL,
        auth_url=AUTH_URL
    )
    api_manager.auth_api.login_user({
        "email": "api1@gmail.com",
        "password": "asdqwe123Q",
    })
    yield api_manager
    session.close()


@pytest.fixture(scope="session")
def api_manager_noauth():
    session = requests.Session()
    api_manager = ApiManager(
        http_session=session,
        headers=DEFAULT_HEADERS,
        api_url=API_URL,
        auth_url=AUTH_URL
    )
    yield api_manager
    session.close()


@pytest.fixture(scope="function")
def create_movie(api_manager_su):
    new_movie = DataGenerator.new_movie()
    response = api_manager_su.movies_api.create_movie(new_movie)
    movie_created = response.json()
    return movie_created


@pytest.fixture(scope="session")
def faker_fxtr() -> Faker:
    return Faker()
