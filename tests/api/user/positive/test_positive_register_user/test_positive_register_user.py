import allure

from tests.api.user.testconstants import allure_feature
from tests.testconstants import allure_epic, QA_ILYA_INITIALS
from positive_register_user_constants import allure_file_description


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Позитив тест регистрация пользователя")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestUserPositiveRegister:
    def test_register_user(self, noauth_session, new_user_common_session):
        user_data = new_user_common_session.payload
        response = new_user_common_session.response

        with allure.step(
            "Проверяем что email созданного пользователя соответствует отправленному"
        ):
            assert response.email == user_data.email, (
                "В ответе при регистрации сервер вернул не тот email, что был отправлен"
            )
