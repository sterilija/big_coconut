from faker import Faker

from models.model import CreateMovieDto, Location

faker = Faker()


class DataGenerator:

    @staticmethod
    def new_movie(**kwargs):
        fake = Faker()
        movie_obj = CreateMovieDto(
            name=kwargs.get("name") or fake.sentence(nb_words=5, variable_nb_words=True),
            price=kwargs.get("price") or fake.random_int(),
            description=kwargs.get("description") or fake.text(max_nb_chars=110),
            location=Location.SPB,
            published=kwargs.get("is_published") or fake.boolean(),
            genreId=kwargs.get("genreId") or 1
        )
        return movie_obj.model_dump(mode="json")

    @staticmethod
    def too_big_number():
        return faker.random_int()**1000