import pytest
from requests import Session
from api.api_manager import ApiManager
from constants import DEFAULT_HEADERS, API_URL, AUTH_URL
from tools.data_generator import DataGenerator

@pytest.fixture(scope="session")
def create_api_manager():
    def new_api_manager():
        session = Session()
        api_manager = ApiManager(
            session=session,
            headers=DEFAULT_HEADERS,
            api_url=API_URL,
            auth_url=AUTH_URL
        )
        return api_manager
    yield new_api_manager

@pytest.fixture(scope="session")
def api_manager_su(create_api_manager):
    api_manager = create_api_manager()
    api_manager.auth_api.login_user({
        "email": "api1@gmail.com",
        "password": "asdqwe123Q",
    })
    yield api_manager


@pytest.fixture(scope="session")
def api_manager_noauth(create_api_manager):
    api_manager = create_api_manager()
    yield api_manager


@pytest.fixture
def create_movie(api_manager_su):
    class CreateMovie:
        def __init__(self):
            self.payload= DataGenerator.new_movie()
            response = api_manager_su.movies_api.create_movie(self.payload)
            self.response = response.json()
    yield CreateMovie()
    del CreateMovie