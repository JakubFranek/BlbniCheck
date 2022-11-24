from datetime import datetime
from typing import Literal

from src.models.task import Task
from src.utilities.event import Event


class Model:
    def __init__(self) -> None:
        self._task_list = []

        self.event_task_added = Event()
        self.event_task_list_loaded = Event()
        self.event_task_deleted = Event()
        self.event_task_edited = Event()

    @property
    def task_list(self) -> list[Task]:
        return self._task_list

    def add_task(
        self, description: str, notes: str | None, date_due: datetime | None
    ) -> None:
        task = Task(description, notes, date_due)
        self.task_list.append(task)
        self.event_task_added()

    def delete_task(self, index: int) -> None:
        del self.task_list[index]
        self.event_task_deleted()

    def edit_task(
        self,
        index: int,
        description: str | Literal[False],
        notes: str | None | Literal[False],
        date_due: datetime | None | Literal[False],
    ) -> None:
        task = self.task_list[index]
        if description is not False:
            task.description = description
        if notes is not False:
            task.notes = notes
        if date_due is not False:
            task.date_due = date_due
        self.event_task_edited()

    def load_task_list(self, task_list: list[Task]) -> None:
        self._task_list = task_list
        self.event_task_list_loaded()
