import json

import allure
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete
from models.db.user_db_model import UserDBModel
from models.db.movie_db_model import MovieDBModel
from tools.datetime_serializer import datetime_serializer


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    """Класс с методами для работы с БД в тестах"""

    def create_db_user(self, user_json: dict):
        with allure.step("Создаём пользователя в БД"):
            user = UserDBModel(**user_json)
            self.db_session.add(user)
            self.db_session.commit()
            self.db_session.refresh(user)

            stmt = insert(UserDBModel).values(**user_json)
            sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                json.dumps(user_json, indent=4, ensure_ascii=False, default=str),
                name="Данные пользователя",
                attachment_type=allure.attachment_type.JSON,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            return user

    def get_user_by_id(self, user_id: str):
        with allure.step("Получаем пользователя по ID из БД"):
            query = self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id)
            user = query.first()

            sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                str(user_id),
                name="ID пользователя",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(
                    user, indent=4, ensure_ascii=False, default=datetime_serializer
                ),
                name="Ответ БД",
                attachment_type=allure.attachment_type.JSON,
            )

            return user

    def get_user_by_email(self, email: str):
        with allure.step("Получаем пользователя по email из БД"):
            query = self.db_session.query(UserDBModel).filter(
                UserDBModel.email == email
            )
            user = query.first()

            sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                str(email),
                name="email пользователя",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(user, indent=4, ensure_ascii=False),
                name="Ответ БД",
                attachment_type=allure.attachment_type.JSON,
            )

            return user

    def get_movie_by_name(self, name: str):
        with allure.step("Получаем фильм из БД по названию"):
            query = self.db_session.query(MovieDBModel).filter(
                MovieDBModel.name == name
            )
            movie: MovieDBModel | None = query.first()

            sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                str(name),
                name="Имя фильма",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            if movie is not None:
                allure.attach(
                    movie.to_json(),
                    name="Ответ БД",
                    attachment_type=allure.attachment_type.JSON,
                )
            else:
                allure.attach(
                    "None", name="Ответ БД", attachment_type=allure.attachment_type.TEXT
                )

            return movie

    def get_movie_by_id(self, movie_id: str):
        with allure.step("Получаем фильм из БД по ID"):
            query = self.db_session.query(MovieDBModel).filter(
                MovieDBModel.id == movie_id
            )
            movie: MovieDBModel | None = query.first()

            sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                str(movie_id),
                name="ID фильма",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            if movie is not None:
                allure.attach(
                    movie.to_json(),
                    name="Ответ БД",
                    attachment_type=allure.attachment_type.JSON,
                )
            else:
                allure.attach(
                    "None", name="Ответ БД", attachment_type=allure.attachment_type.TEXT
                )

            return movie

    def user_exists_by_email(self, email: str) -> bool:
        with allure.step("Проверяем по email, существует ли пользователь в БД"):
            query = self.db_session.query(UserDBModel).filter(
                UserDBModel.email == email
            )

            sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            allure.attach(
                str(email),
                name="email пользователя",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                sql, name="SQL-запрос", attachment_type=allure.attachment_type.TEXT
            )

            user_exists = query.count() > 0
            return user_exists

    def delete_user(self, user: UserDBModel):
        stmt = delete(UserDBModel).where(UserDBModel.id == user.id)
        sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))

        with allure.step("Удаляем пользователя через БД"):
            allure.attach(
                json.dumps(user.convert_to_dict(), indent=4, ensure_ascii=False),
            )
            allure.attach(
                sql,
                name="SQL запрос",
                attachment_type=allure.attachment_type.TEXT,
            )

            self.db_session.delete(user)
            self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    '''
    Пример хелпера для movies
    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()
    '''
