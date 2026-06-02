from typing import Generator

import pytest
from sqlalchemy.orm import Session
from modules.db.db_client import get_db_session
from modules.db.db_helper import DBHelper


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture
def db_helper(db_session: Session) -> Generator[DBHelper, None, None]:
    """
    Фикстура для экземпляра хелпера
    """
    db_session = get_db_session()
    db_helper = DBHelper(db_session)
    yield db_helper
