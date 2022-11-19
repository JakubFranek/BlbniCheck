from datetime import datetime

import pytest

from src.models.task import Task


def test_init_pass():
    task_desc = "A Test Task"
    task_notes = "Some extra notes"

    dt_now = datetime.now()

    task = Task(task_desc, task_notes)

    dt_diff = task.date_created - dt_now

    assert task.description == task_desc
    assert task.notes == task_notes
    assert isinstance(task.date_created, datetime)
    assert dt_diff.seconds < 1


def test_init_long_desc_fail():
    task_desc = "A" * 50
    task_notes = "Some extra notes"

    with pytest.raises(ValueError):
        Task(task_desc, task_notes)
