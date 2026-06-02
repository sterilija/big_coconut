import pytest
import allure
from tests.testconstants import allure_epic, QA_ILYA_INITIALS
from tests.api.user.testconstants import allure_feature
from negative_register_user_constants import allure_file_description, test_data
from tools.assert_response_message import assert_response_message


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест регистрация пользователя")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestUserRegisterNegative:
    @allure.title(test_data.title)
    @pytest.mark.parametrize(
        argnames=test_data.parameters.arg_names,
        argvalues=test_data.parameters.arg_values,
        ids=test_data.parameters.ids,
    )
    def test_register_user_wrong_data(
        self, su_session, payload, expected_status, assertion_message, expected_message
    ):
        server_response = su_session.user_api.register_user(
            user_json=payload, expected_status=expected_status
        )

        assert_response_message(
            reason="Попытка зарегать пользователя, отправив неверные данные, проверяем ответ",
            expected_message=expected_message,
            response_message=server_response.message,
            checking_type="in",
            assertion_message=assertion_message,
        )
