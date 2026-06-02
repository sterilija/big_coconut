class RequiredTypes:
    BOOL = "булевым значением"
    STRING = "строкой"
    NUMBER = "числом"
    INTEGER = "целым числом"


class FilmErrors:
    FILM_NOT_FOUND = "Фильм не найден"
    FILM_WITH_THE_NAME_ALREADY_EXISTS = "Фильм с таким названием уже существует"


class NameErrors:
    NAME_SHOULD_NOT_BE_EMPTY = "name should not be empty"


class AccessErrors:
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN_RESOURCE = "Forbidden resource"


class EmailErrors:
    INCORRECT_EMAIL = "Некорректный email"


class PasswordErrors:
    MIN_PASSWORD_LENGTH = "Минимальная длина пароля 8 символов"
    PASSWORD_SHOULD_NOT_BE_EMPTY = "Поле пароля не должно быть пустым"
    PASSWORD_SHOULD_HAVE_CAPITALS = (
        "Пароль должен содержать хотя бы одну заглавную букву"
    )


class FIOErrors:
    FIO_SHOULD_HAVE_ONLY_LETTERS_AND_SPACES = (
        "Поле ФИО должно содержать только буквы и пробелы"
    )
    FIO_MIN_LENGTH = "Минимальная длина поля ФИО 5 символов"
    FIO_SHOULD_NOT_BE_EMPTY = "Поле ФИО не должно быть пустым"


class MiscErrorMessages:
    WRONG_DATA = "Некорректные данные"
    INTERNAL_ERROR = "Internal server error"


class ServerErrorMessages(MiscErrorMessages):
    Film_errors = FilmErrors
    PasswordErrors = PasswordErrors
    FIOErrors = FIOErrors
    EmailErrors = EmailErrors
    NameErrors = NameErrors
    AccessErrors = AccessErrors

    @staticmethod
    def field_must_be_type(field: str, required_type: str) -> str:
        return f"Поле {field} должно быть {required_type}"

    @staticmethod
    def field_must_be_not_less_than(field: str, bigger_value: int | str) -> str:
        return f"{field} must not be less than {bigger_value}"

    @staticmethod
    def field_must_be_less_than(field: str, bigger_value: int | str) -> str:
        return f"{field} must be less than {bigger_value}"

    @staticmethod
    def field_has_maximum_amount(field: str, amount: int) -> str:
        return f"Поле {field} имеет максимальную величину {amount}"

    @staticmethod
    def field_must_be_more_than(field: str, amount: int):
        return f"Поле {field} должно быть больше {amount}"

    @staticmethod
    def field_has_minimum_amount(field: str, amount: int) -> str:
        return f"Поле {field} имеет минимальную величину {amount}"

    @staticmethod
    def field_must_be_one_of_rus(field: str, values_list: list[str]) -> str:
        return f"Поле {field} должно быть одним из: {', '.join(values_list)}"

    @staticmethod
    def field_must_be_one_of_eng(field: str, values_list: list[str]) -> str:
        return f"{field} must be one of the following values: {', '.join(values_list)}"

    @staticmethod
    def field_cannot_be_empty(field: str):
        return f"Поле {field} не может быть пустым"
