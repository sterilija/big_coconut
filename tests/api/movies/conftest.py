import pytest
import allure

from tools.data_generator import DataGenerator


@pytest.fixture
def session(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def create_movie(su_session):
    with allure.step("Генерируем новый фильм фикстурой"):

        class CreateMovie:
            def __init__(self):
                self.payload = DataGenerator.new_movie()
                self.response_model = su_session.movies_api.create_movie(self.payload)

        yield CreateMovie()
    del CreateMovie
