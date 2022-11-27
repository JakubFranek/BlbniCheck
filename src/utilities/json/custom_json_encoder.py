import json
from datetime import datetime
from decimal import Decimal
from typing import Any

from src.models.task import Task


class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: U100
        super().__init__(indent=2, separators=(", ", ": "))

    def default(self, arg: Any) -> Any:
        if isinstance(arg, datetime):
            return arg.isoformat()
        elif isinstance(arg, Task):
            date_due = arg.date_due.isoformat() if arg.date_due is not None else "None"
            date_done = (
                arg.date_done.isoformat() if arg.date_done is not None else "None"
            )
            return {
                "datatype": "Task",
                "description": arg.description,
                "notes": arg.notes,
                "done": arg.done,
                "date_due": date_due,
                "date_created": arg.date_created.isoformat(),
                "date_done": date_done,
            }
        elif isinstance(arg, Decimal):
            return {"datatype": "Decimal", "number": str(arg)}
        else:
            super().default(arg)
