from faker import Faker

from tests.testconstants import TestInitials, TestParameters

allure_file_description = """
    Тестирование позитивных сценариев получения фильма.
    В этом файле в каждом тесте присутствует также тест всех ролёвок в рамках позитивных сценариев
    Тесты, присутствующе в этом файле:
    1. (парам.) test_get_movie - Получение фильма по id с ролёвками
    2. (парам.) test_get_movies_list_no_query - Получение списка фильмов без заданных параметров поиска
    3. (парам.) test_get_movies_list - Получение списка фильмов с заданными параметрами поиска
    4. (парам.) test_get_movies_list_positive_pagination_boundaries - Получение списка фильмов на граничных значениях пагинации
    5. (парам.) test_get_movies_list_check_sorting - Проверка сортировки выдачи фильмов
    """

fake = Faker()


class TestsList:
    get_movie = TestInitials(
        title='Получение фильма по ID из роли "{param_id}"',
        description="Здесь мы получаем фильм, созданный фикстурой, по id",
        parameters=TestParameters(
            arg_names="parameter_session",
            arg_values=["su_session", "new_user_common_session"],
            indirect=True,
        ),
    )
    get_movies_list_no_query = TestInitials(
        title='Получение фильмов без query-параметров из роли "{param_id}"',
        description="Здесь мы получаем список всех фильмов, так как query пуст",
        parameters=TestParameters(
            arg_names="parameter_session",
            arg_values=["su_session", "new_user_common_session"],
            indirect=True,
        ),
    )
    get_movies_list = TestInitials(
        title='Получение фильмов с заданными query-параметрами из роли "{param_id}"',
        parameters=TestParameters(
            arg_names="parameter_session",
            arg_values=["su_session", "new_user_common_session"],
            indirect=True,
        ),
    )
    get_movies_list_positive_pagination_boundaries = TestInitials(
        title="Получение фильмов на пограничных значениях пагинации",
        parameters=TestParameters(
            arg_names="page, page_size",
            arg_values=[(1, 1), (fake.random_int(max=20, min=1), 20)],
        ),
    )
    get_movies_list_check_sorting = TestInitials(
        title="Получение списка фильмов и проверка их сортировки по дате создания",
        parameters=TestParameters(
            arg_names="sorting, reversed_check",
            arg_values=[("asc", False), ("desc", True)],
        ),
    )
