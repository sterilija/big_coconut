from typing import Sequence, Iterable

from _pytest.mark import ParameterSet

QA_ILYA_INITIALS = ("qa_name", "Илья Алексеевич")
allure_epic = "Реализация сервиса Cinescope"


class TestParameters:
    def __init__(
        self,
        arg_names: str | Sequence[str],
        arg_values: Iterable[ParameterSet | Sequence[object] | object],
        indirect: bool | Sequence[str] = ...,
        ids: Iterable[None | str | float | int | bool] = ...,
    ):
        self.arg_names = arg_names
        self.arg_values = arg_values
        self.indirect = indirect
        self.ids = ids


class TestInitials:
    def __init__(
        self,
        title: str,
        description: str | None = ...,
        parameters: TestParameters | None = ...,
    ):
        self.title = title
        self.description = description
        self.parameters = parameters
