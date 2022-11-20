from datetime import datetime

from src.models.task import Task


class Model:
    def __init__(self, task_list: list[Task] | None = None) -> None:
        if task_list is not None:
            self.load_task_list(task_list)
        else:
            self._task_list = []

    @property
    def task_list(self) -> list[Task]:
        return self._task_list

    def add_task(self, description: str, notes: str, date_due: datetime) -> None:
        task = Task(description, notes, date_due)
        self.task_list.append(task)

    def remove_task(self) -> None:
        pass

    def edit_task(self) -> None:
        pass

    def load_task_list(self, task_list: list[Task]) -> None:
        self._task_list = task_list
