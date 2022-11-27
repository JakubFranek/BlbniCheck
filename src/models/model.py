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
        changed = False

        if description is not False and description != task.description:
            task.description = description
            changed = True
        if notes is not False and notes != task.notes:
            task.notes = notes
            changed = True
        if date_due is not False and date_due != task.date_due:
            task.date_due = date_due
            changed = True

        if changed is True:
            self.event_task_edited()

    def set_task_status(self, index: int, status: bool) -> None:
        if status != self.task_list[index].done:
            self.task_list[index].done = status
            self.event_task_edited()

    def load_task_list(self, task_list: list[Task]) -> None:
        self._task_list = task_list
        self.event_task_list_loaded()
