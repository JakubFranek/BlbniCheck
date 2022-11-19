from datetime import datetime
from typing import Optional

from src.utilities.validation.validation import validate_string


class Task:
    MAX_DESCRIPTION_LENGTH = 32
    MIN_DESCRIPTION_LENGTH = 1

    MAX_NOTES_LENGTH = 256
    MIN_NOTES_LENGTH = 0

    def __init__(
        self,
        description_arg: str,
        notes_arg: Optional[str] = None,
        date_due_arg: Optional[datetime] = None,
    ) -> None:

        self.description = description_arg
        self.notes = notes_arg
        self.date_due = date_due_arg

        self._date_created: datetime = datetime.now()
        self.done = False

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description: str = validate_string(
            value,
            "Task description",
            Task.MIN_DESCRIPTION_LENGTH,
            Task.MAX_DESCRIPTION_LENGTH,
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value: Optional[str]) -> None:
        if value is None:
            self._notes = None
        else:
            self._notes = validate_string(
                value, "Task notes", Task.MIN_NOTES_LENGTH, Task.MAX_NOTES_LENGTH
            )

    @property
    def date_due(self) -> Optional[datetime]:
        return self._date_due

    @date_due.setter
    def date_due(self, value: Optional[datetime]) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("Task due date must be a datetime or a None.")
        self._date_due: Optional[datetime] = value

    @property
    def date_created(self) -> datetime:
        return self._date_created

    @property
    def date_done(self) -> Optional[datetime]:
        return self._date_done

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool) -> None:
        if value is False:
            self._date_done = None
            self._done = False
        else:
            self._date_done = datetime.now()
            self._done = True
