import allure
import pytest
from requests import Session
from modules.api.api_manager import ApiManager
from constants.browser import DEFAULT_HEADERS, API_URL, AUTH_URL
from constants.roles import Roles
from entities.user import User
from dotenv import load_dotenv
from os import getenv
from typing import Callable, Generator

from tools.data_generator import DataGenerator

load_dotenv()


class SuperAdminCreds:
    USERNAME = getenv("SUPER_ADMIN_USERNAME")
    PASSWORD = getenv("SUPER_ADMIN_PASSWORD")


@pytest.fixture(scope="session")
def create_api_manager() -> Generator[Callable[[], ApiManager], None, None]:
    def new_api_manager() -> ApiManager:
        session = Session()
        api_manager = ApiManager(
            session=session, headers=DEFAULT_HEADERS, api_url=API_URL, auth_url=AUTH_URL
        )
        return api_manager

    yield new_api_manager


@pytest.fixture(scope="session")
def create_user_session(
    create_api_manager,
) -> Generator[Callable[[], ApiManager], None, None]:
    user_pool = []

    def _create_user_session() -> ApiManager:
        with allure.step("Создаём сессию"):
            user_session = create_api_manager()
            user_pool.append(user_session)
            return user_session

    yield _create_user_session

    for session_of_user in user_pool:
        session_of_user.close_session()


@pytest.fixture(scope="session")
def su_session(create_user_session) -> Generator[ApiManager, None, None]:
    with allure.step("Инициализируем фикстуру сессии супер-пупер пользователя"):
        session = create_user_session()

        su_user = User(
            email=SuperAdminCreds.USERNAME,
            password=SuperAdminCreds.PASSWORD,
            session=session,
            roles=[Roles.SUPER_ADMIN.value],
        )

        su_user.session.user_api.login_user(su_user.creds)

    yield session


@pytest.fixture(scope="session")
def noauth_session(create_user_session) -> Generator[ApiManager, None, None]:
    with allure.step("Инициализируем фикстуру сессии неавторизованного товарища"):
        yield create_user_session()


@pytest.fixture
def new_user_common_session(create_user_session, su_session):

    with allure.step("Инициализируем фикстуру сессии обычного пользователя"):

        class UserCreated:
            def __init__(self):
                session = create_user_session()
                user_data = DataGenerator.new_user_data_validated_model()

                user = User(
                    email=user_data.email,
                    password=user_data.password,
                    roles=user_data.roles,
                    session=session,
                )

                user_response = su_session.user_api.register_user(user_data)
                user.session.user_api.login_user(user.creds)

                self.payload = user_data
                self.response = user_response
                self.session = session

            def __getattr__(self, item):
                return getattr(self.session, item)

    yield UserCreated()
    del UserCreated


@pytest.fixture
def parameter_session(request):
    return request.getfixturevalue(request.param)
