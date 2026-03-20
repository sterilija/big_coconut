from faker import Faker

from models.model import CreateMovieDto, Location


class DataGenerator:

    @staticmethod
    def new_movie():
        fake = Faker()
        movie_json = CreateMovieDto(
            name=fake.sentence(nb_words=5, variable_nb_words=True),
            price=fake.random_int(),
            description=fake.text(max_nb_chars=110),
            location=Location.SPB,
            published=fake.boolean(),
            genreId=1
        )
        return movie_json


news = DataGenerator.new_movie()
print(news.model_dump())