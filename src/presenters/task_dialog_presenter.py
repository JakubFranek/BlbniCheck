import logging
from datetime import datetime

from src.models.model import Model
from src.utilities.handle_exception import handle_exception
from src.views.task_dialog import TaskDialog
from src.views.view_models.task_table_model import TaskTableModel


class TaskDialogPresenter:
    def __init__(self, model: Model, table_model: TaskTableModel) -> None:
        self.model = model
        self.table_model = table_model

    def create_dialog(self) -> None:
        self.dialog = TaskDialog()
        self.dialog.signal_ok.connect(self.create_task)
        self.dialog.signal_apply.connect(self.create_task)
        logging.info("Running TaskDialog")
        self.dialog.exec()

    def create_task(self) -> None:
        description = self.dialog.description
        notes = self.dialog.notes
        date_due = datetime.strptime(self.dialog.date_due, "%d.%m.%Y %H:%M")

        try:
            self.table_model.pre_add()
            self.model.add_task(description, notes, date_due)
            self.table_model.post_add()
            logging.info(f'Task "{description}" added')
            self.dialog.accept()
        except Exception as exc:
            display_text, display_details = handle_exception(exc)  # type: ignore
            self.dialog.display_error(display_text, display_details)
