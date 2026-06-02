from tools.data_generator import DataGenerator
from tools.compare_dicts_by_keys import compare_dicts_by_keys
from modules.db.db_helper import DBHelper
import allure


@allure.epic("Реализация сервиса Cinescope")
@allure.feature("Тест работоспособности БД")
@allure.story("Позитив тест создания колонки пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestDBCreateUserColumn:
    def test_db_create_user_column(self, db_helper: DBHelper):
        user_data = DataGenerator.new_db_user_data()
        user_id = user_data.get("id")
        comparable_keys = list(user_data.keys())
        comparable_keys.remove("created_at")
        comparable_keys.remove("updated_at")

        db_response = db_helper.create_db_user(user_data)
        creation_response = db_response.convert_to_dict()
        db_response = db_helper.get_user_by_id(user_id)
        get_response = db_response.convert_to_dict()

        compare_dicts_by_keys(
            reason="Создали пользователя в БД, проверяем ответ с отправленными данными",
            dict_original=user_data,
            dict_expected=creation_response,
            keys=comparable_keys,
            exception_message="Ответ от БД при записи данных пользователя не соответств. переданным данным",
        )
        compare_dicts_by_keys(
            reason="Создали пользователя в БД, получили, проверяем схожесть с отправленными данными",
            dict_original=creation_response,
            dict_expected=get_response,
            keys=comparable_keys,
            exception_message="Ответ от БД при получении данных пользователя не соответств. переданным данным",
        )
