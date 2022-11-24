import json
from datetime import datetime
from decimal import Decimal
from typing import Any

from src.models.task import Task


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> Any:
        if "datatype" in obj:
            if obj["datatype"] == "Decimal":
                return Decimal(obj["number"])
            elif obj["datatype"] == "Task":
                description = obj["description"]
                notes = obj["notes"]
                done = obj["done"]
                temp_date_due = obj["date_due"]
                date_created = obj["date_created"]
                if temp_date_due == "None":
                    date_due = None
                else:
                    date_due = datetime.fromisoformat(temp_date_due)
                task = Task(description, notes, date_due)
                task._date_created = datetime.fromisoformat(date_created)
                task.done = done
                return task
        return obj
