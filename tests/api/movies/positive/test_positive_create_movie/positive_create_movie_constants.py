from tests.testconstants import TestInitials

allure_file_description = """
    Тестирование позитивных сценариев создания фильма.
    Тесты, присутствующе в этом файле:
    1. test_create_movie_fixture_su - Создание фильма с помощью фикстуры
    2. test_create_movie_su - Создание фильма через API ручку
    """


class TestsList:
    create_movie_fixture_su = TestInitials(title="Создание фильма через фикстуру")
    create_movie_su = TestInitials(title="Создание фильма через API ручку")
