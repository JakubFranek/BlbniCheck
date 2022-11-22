from datetime import datetime

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
    ) -> int:
        """Adds a new Task (pending validation within Task properties) to the task_list
        and returns the index at which the new Task was added to the task_list. Fires
        the event_task_added Event.

        Args:
            description (str): short description of the Task (a name)
            notes (str | None, optional): longer, multi-line note text
            date_due (datetime | None, optional): date due for the Task

        Returns:
            int: the index of the newly added Task within task_list
        """
        task = Task(description, notes, date_due)
        self.task_list.append(task)
        self.event_task_added()
        return len(self.task_list) - 1

    def delete_task(self, index: int) -> None:
        del self.task_list[index]
        self.event_task_deleted()

    def edit_task(self) -> None:
        self.event_task_edited()

    def load_task_list(self, task_list: list[Task]) -> None:
        self._task_list = task_list
        self.event_task_list_loaded()
