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
        self.dialog.signal_apply.connect(lambda: self.create_task(False))
        self.dialog.signal_cancel.connect(lambda: self.close_dialog(False))
        self.dialog.signal_date_due_toggle.connect(self.date_due_toggled)

        logging.info("Running TaskDialog...")
        self.dialog.exec()

    def create_task(self, close_dialog: bool = True) -> None:
        logging.info("Adding a new Task...")
        description = self.dialog.description
        notes = self.dialog.notes
        if self.dialog.date_due_enabled is True:
            date_due = datetime.strptime(self.dialog.date_due, "%d.%m.%Y %H:%M")
        else:
            date_due = None

        try:
            index = len(self.model.task_list)
            self.table_model.pre_add()
            self.model.add_task(description, notes, date_due)
            self.table_model.post_add()
            logging.info(f'Task "{description}" added at index {index}')
            if close_dialog is True:
                self.close_dialog(True)
        except Exception:
            self.handle_exception()

    def close_dialog(self, accepted: bool) -> None:
        if accepted is True:
            logging.info("Closing TaskDialog (result 'Accepted')")
            self.dialog.accept()
        else:
            logging.info("Closing TaskDialog (result 'Rejected')")
            self.dialog.reject()

    def date_due_toggled(self) -> None:
        if self.dialog.date_due_enabled is True:
            self.dialog.dateTimeEditDueDate.setEnabled(True)
        else:
            self.dialog.dateTimeEditDueDate.setEnabled(False)

    def handle_exception(self) -> None:
        display_text, display_details = handle_exception()  # type: ignore
        self.dialog.display_error(display_text, display_details)
