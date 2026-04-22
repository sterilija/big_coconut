from faker import Faker

import allure

from models.api.movies_model import Location
from random import choice
from uuid import uuid4
from datetime import datetime

from models.api.user_model import CreateUserDto

faker = Faker()


class DataGenerator:
    @staticmethod
    def new_movie(
        **kwargs,
    ):
        fake = Faker()

        with allure.step("Генерируем данные для фильма"):
            movie = {
                "name": fake.sentence(nb_words=5),
                "price": fake.random_int(),
                "description": fake.text(max_nb_chars=110),
                "location": DataGenerator.random_location(),
                "published": fake.boolean(),
                "genreId": 1,
                "imageUrl": "https://example.com/image.png",
            }

        movie.update(kwargs)

        return movie

    @staticmethod
    def random_location():
        return choice([Location.SPB, Location.MSK]).value

    @staticmethod
    def too_big_number() -> int:
        big_number = faker.random_int() ** 1000
        return big_number

    @staticmethod
    def new_user_data(**kwargs):
        fake = Faker()
        password = fake.password()

        user_obj = {
            "email": kwargs.get("email") or fake.email(),
            "password": kwargs.get("password") or password,
            "passwordRepeat": kwargs.get("password") or password,
            "fullName": kwargs.get("fullname") or fake.name(),
        }

        user_obj.update(kwargs)

        return user_obj

    @staticmethod
    def new_user_data_validated_model(**kwargs: CreateUserDto | None):
        user_data = DataGenerator.new_user_data(**kwargs)

        return CreateUserDto(**user_data)

    @staticmethod
    def new_db_user_data(**kwargs):
        pregenerated_user = DataGenerator.new_user_data_validated_model()

        user_data = {
            "id": str(uuid4()),
            "email": pregenerated_user.email,
            "full_name": pregenerated_user.fullName,
            "password": pregenerated_user.password,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "verified": pregenerated_user.verified,
            "banned": pregenerated_user.banned,
            "roles": "{USER}",
        }

        user_data.update(kwargs)

        return user_data
