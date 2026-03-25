import pytest
import requests
from api.api_manager import ApiManager
from constants import DEFAULT_HEADERS, API_URL, AUTH_URL
from tools.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session_new():
    session =  requests.Session()
    yield session
    session.close()

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

@pytest.fixture(scope="function")
def create_movie(api_manager_su):
    new_movie = DataGenerator.new_movie()
    response = api_manager_su.movies_api.create_movie(new_movie)
    movie_created = response.json()
    return movie_created