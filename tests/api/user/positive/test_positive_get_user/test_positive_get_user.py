from models.api.user_model import UserResponse
from modules.api.api_manager import ApiManager
from positive_get_user_constants import (
    allure_file_description,
    TestsList,
)
import allure
from tests.testconstants import QA_ILYA_INITIALS
from tests.testconstants import allure_epic
from tests.api.user.testconstants import allure_feature
from tools.compare_dicts_by_keys import compare_dicts_by_keys


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив тест получение пользователя")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestUserPositiveGet:
    @allure.title(TestsList.user_get_by_id.title)
    def test_user_get_by_id(self, new_user_common_session, su_session: ApiManager):
        user_id = new_user_common_session.response.id
        user_creation_response = new_user_common_session.response.model_dump(
            mode="python"
        )

        user_response_model = su_session.user_api.get_user(user_id)
        user_response_dict = user_response_model.model_dump(mode="python")

        compare_dicts_by_keys(
            dict_original=user_creation_response,
            dict_expected=user_response_dict,
            keys=UserResponse.model_fields.keys(),
            reason="Создали пользователя фикстурой, получили его по ID, проверяем схожесть",
            exception_message="Полученный пользователь по ID не соответствует созданному",
        )

    @allure.title(TestsList.user_get_by_email.title)
    def test_user_get_by_email(self, new_user_common_session, su_session: ApiManager):
        user_email = new_user_common_session.response.email
        user_creation_response = new_user_common_session.response.model_dump(
            mode="python"
        )

        user_response_model = su_session.user_api.get_user(user_email)
        user_response_dict = user_response_model.model_dump(mode="python")

        compare_dicts_by_keys(
            dict_original=user_creation_response,
            dict_expected=user_response_dict,
            keys=UserResponse.model_fields.keys(),
            reason="Создали пользователя фикстурой, получили его по email, проверяем схожесть",
            exception_message="Полученный пользователь по email не соответствует созданному",
        )

    @allure.title(TestsList.get_users_list.title)
    def test_get_users_list(self, su_session: ApiManager):
        users_response = su_session.user_api.get_user("")

        with allure.step("Проверяем что ответ не пуст"):
            assert len(users_response.users) > 0, "ручка users не выдала список юзеров"
