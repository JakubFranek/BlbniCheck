from typing import List, Optional

from src.models.task import Task


class Model:
    def __init__(self, task_list: Optional[List[Task]] = None) -> None:
        if task_list is not None:
            self.load_task_list(task_list)

    @property
    def task_list(self) -> list:
        if self._task_list:
            return self._task_list
        else:
            return []

    def add_task(self):
        pass

    def remove_task(self):
        pass

    def edit_task(self):
        pass

    def load_task_list(self, task_list: List[Task]):
        self._task_list = task_list
