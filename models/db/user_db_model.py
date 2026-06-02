from typing import Dict, Any

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserDBModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(DateTime)
    verified: Mapped[bool] = mapped_column(Boolean)
    banned: Mapped[bool] = mapped_column(Boolean)
    roles: Mapped[str] = mapped_column(String)

    def convert_to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "verified": self.verified,
            "banned": self.banned,
            "roles": self.roles,
        }

    def get_keys(self) -> list[str]:
        keys = [column.key for column in self.__tablename__.columns]
        return keys

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"
