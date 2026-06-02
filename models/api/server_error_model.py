from http import HTTPStatus
from typing import Optional

from datamodel_code_generator.model.enum import Enum
from pydantic import BaseModel


class Error(Enum):
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN_RESOURCE = "Forbidden resource"
    INTERNAL_ERROR = "Internal server error"
    WRONG_DATA = "Некорректные данные"
    BAD_REQUEST = "Bad Request"


class ErrorMessage(BaseModel):
    message: str | list[str]
    statusCode: HTTPStatus
    error: Optional[str] = Error
