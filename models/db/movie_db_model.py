import json
from typing import Dict, Any

from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


rename_map = {"image_url": "imageUrl", "genre_id": "genreId", "created_at": "createdAt"}


class MovieDBModel(Base):
    __tablename__ = "movies"

    id: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = mapped_column()
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(Integer)
    created_at = Column(DateTime)

    def __rename_keys_to_api_comparable(self, movie_dict):
        for k, v in rename_map.items():
            movie_dict[v] = movie_dict.pop(k)

    def convert_to_dict(self, api_comparable: Boolean = True) -> Dict[str, Any]:
        """
        Преобразование в словарь
        Args:
            api_comparable(Boolean):
                Меняет названия ключей фильма под соответствие тем что
                используются в API (Пример: Вместо "genre_id" будет "genreId")
        """
        movie = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "location": self.location,
            "published": self.published,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at.isoformat(),
        }
        if api_comparable:
            self.__rename_keys_to_api_comparable(movie)

        return movie

    def to_json(self):
        dicted = self.convert_to_dict()
        return json.dumps(
            dicted,
            indent=4,
            ensure_ascii=False,
            default=str,
        )

    def get_column_names(self, api_comparable=True) -> list[str]:
        keys = list(self.__table__.columns.keys())

        if api_comparable:
            keys = [rename_map.get(key, key) for key in keys]

        return keys

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"
