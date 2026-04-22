import pytest
import allure
from tests.testconstants import allure_epic, QA_ILYA_INITIALS
from tests.api.user.testconstants import allure_feature
from negative_get_user_constants import (
    allure_file_description,
    TestsList,
    STP_ERROR_COMPARISON_MSG,
)
from tools.assert_response_message import assert_response_message


@allure.epic(allure_epic)
@allure.feature(allure_feature)
@allure.story("Негатив тест получение пользователя")
@allure.description(allure_file_description)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label(QA_ILYA_INITIALS)
class TestUserNegativeGet:
    @allure.title(TestsList.get_users_list_wrong_query.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_users_list_wrong_query.parameters.arg_names,
        argvalues=TestsList.get_users_list_wrong_query.parameters.arg_values,
        ids=TestsList.get_users_list_wrong_query.parameters.ids,
    )
    def test_get_users_list_wrong_query(
        self, su_session, query, expected_message, expected_status, assertion_message
    ):
        server_response = su_session.user_api.get_user(
            user_locator="", query=query, expected_status=expected_status
        )

        assert_response_message(
            reason="Попытались получить список пользователей с неправ. query-параметрами, проверяем ответ",
            expected_message=expected_message,
            response_message=server_response.message,
            checking_type="in",
            assertion_message=assertion_message,
        )

    @allure.title(TestsList.get_user_wrong_locator.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_user_wrong_locator.parameters.arg_names,
        argvalues=TestsList.get_user_wrong_locator.parameters.arg_values,
        ids=TestsList.get_user_wrong_locator.parameters.ids,
    )
    def test_get_user_wrong_locator(self, su_session, user_id, expected_status):
        response_data = su_session.user_api.get_user(
            user_locator=user_id, expected_status=expected_status
        )

        with allure.step(STP_ERROR_COMPARISON_MSG):
            assert response_data == {}, (
                "Вместо ожидаемого пустотела со статусом 200, ручка GET /user выдала что-то другое"
            )

    @allure.title(TestsList.get_user_wrong_session_role.title)
    @pytest.mark.parametrize(
        argnames=TestsList.get_user_wrong_session_role.parameters.arg_names,
        argvalues=TestsList.get_user_wrong_session_role.parameters.arg_values,
        ids=TestsList.get_user_wrong_session_role.parameters.ids,
        indirect=TestsList.get_user_wrong_session_role.parameters.indirect,
    )
    def test_get_user_wrong_session_role(
        self,
        parameter_session,
        new_user_common_session,
        expected_message,
        expected_status,
    ):
        user_id = new_user_common_session.response.id

        server_response = parameter_session.user_api.get_user(
            user_locator=user_id, expected_status=expected_status
        )

        assert_response_message(
            reason="Попытка создать юзера из-под неправильной роли, проверяем ответ",
            response_message=server_response.message,
            expected_message=expected_message,
            checking_type="in",
            assertion_message="Неправильный ответ в сообщении при попытке получить пользователя через /users без админских прав",
        )
