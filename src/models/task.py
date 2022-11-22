from datetime import datetime

from src.utilities.validation import validate_string


class Task:
    MAX_DESCRIPTION_LENGTH = 32
    MIN_DESCRIPTION_LENGTH = 1

    MAX_NOTES_LENGTH = 256
    MIN_NOTES_LENGTH = 0

    def __init__(
        self,
        description_arg: str,
        notes_arg: str | None = None,
        date_due_arg: datetime | None = None,
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
    def notes(self) -> str | None:
        return self._notes

    @notes.setter
    def notes(self, value: str | None) -> None:
        if value is None:
            self._notes = None
        else:
            self._notes = validate_string(
                value, "Task notes", Task.MIN_NOTES_LENGTH, Task.MAX_NOTES_LENGTH
            )

    @property
    def date_due(self) -> datetime | None:
        return self._date_due

    @date_due.setter
    def date_due(self, value: datetime | None) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("Task due date must be a datetime or a None.")
        self._date_due: datetime | None = value

    @property
    def date_created(self) -> datetime:
        return self._date_created

    @property
    def date_done(self) -> datetime | None:
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
