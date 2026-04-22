import pytest

from models.db.account_transaction_db_model import AccountTransactionTemplate
from faker import Faker

from sqlalchemy.orm import Session
import allure

fake = Faker()


@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами Игуана-Боба")
@allure.story("Корректность перевода денег между двумя счетами")
@allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "Илья Алексеевич")
class TestAccountsTransactionTemplate:
    @allure.title("Тест перевода денег между счетами Игуана-Боба на 200 рублей")
    def test_accounts_transaction_template(self, db_session: Session):
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(
                user=f"Stan_{fake.random_int(10)}", balance=1000
            )

            bob = AccountTransactionTemplate(
                user=f"Bob_{fake.random_int(10)}", balance=500
            )

        # Добавляем записи в сессию
        db_session.add_all([stan, bob])
        # Фиксируем изменения в базе данных
        db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
                    функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
                    и вызывая метод transfer_money, мы как будто-бы делаем запрос в api_manager.movies_api.transfer_money
                    """)
        def transfer_money(session: Session, sender: str, receiver: str, amount: float):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы как будто-бы делаем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param sender: ID счета, с которого списываются деньги.
            :param receiver: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            with allure.step("Получаем счета"):
                sender = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=sender)
                    .one()
                )
                receiver = (
                    session.query(AccountTransactionTemplate)
                    .filter_by(user=receiver)
                    .one()
                )

            with allure.step("Проверяем, что на счете достаточно средств"):
                if sender.balance < amount:
                    raise ValueError("Недостаточно средств")

            with allure.step("Выполняем перевод"):
                sender.balance -= amount
                receiver.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(
                    db_session, sender=stan.user, receiver=bob.user, amount=200
                )
            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()

            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
            with allure.step("Фиксируем изменения в базе данных"):
                db_session.commit()
