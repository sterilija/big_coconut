from tests.testconstants import TestInitials

allure_file_description = """
    Тестирование позитивных сценариев получения пользователя.
    Тесты, присутствующе в этом файле:
    1. test_user_get_by_id - получение пользователя по ID
    2. test_user_get_by_email - получение пользователя по ID
    3. test_get_users_list - получение списка пользователей
    """

USER_ID_MISMATCH_MSG = (
    "id пользователя при получении (get) не соответствует тому что создали"
)
USER_EMAIL_MISMATCH_MSG = (
    "email пользователя при получении (get) не соответствует тому что создали"
)
USER_NAME_MISMATCH_MSG = (
    "полное имя пользователя при получении (get) не соответствует тому что создали"
)


class TestsList:
    user_get_by_id = TestInitials(
        title="Получение пользователя по ID",
    )
    user_get_by_email = TestInitials(title="Получение пользователя по email")
    get_users_list = TestInitials(title="Получение списка пользователей")
