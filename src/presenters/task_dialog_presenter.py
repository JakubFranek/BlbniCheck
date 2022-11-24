import logging
from datetime import datetime

from src.models.model import Model
from src.utilities.handle_exception import handle_exception
from src.views.task_dialog import TaskDialog
from src.views.view_models.task_table_model import TaskTableModel


class TaskDialogPresenter:
    STRING_DIFFERENT_VALUES = "Keep current values"
    STRING_NO_DATE_DUE_SET = "No Date Due set"

    def __init__(self, model: Model, table_model: TaskTableModel) -> None:
        self.model = model
        self.table_model = table_model

    def create_dialog(self, edit_mode: bool) -> None:
        self.dialog = TaskDialog(edit_mode)

        if edit_mode is True:
            self.dialog.signal_ok.connect(self.edit_task)
            self.dialog.signal_apply.connect(lambda: self.edit_task(False))
        else:
            self.dialog.signal_ok.connect(self.create_task)
            self.dialog.signal_apply.connect(lambda: self.create_task(False))
        self.dialog.signal_cancel.connect(lambda: self.close_dialog(False))
        self.dialog.signal_date_due_toggle.connect(self.date_due_toggled)

        if edit_mode is True:
            self.populate_widgets()

        logging.info(f"Running TaskDialog ({edit_mode=})...")
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

    def edit_task(self, close_dialog: bool = True) -> None:
        indices = self.table_model.get_selected_source_rows()
        logging.info(f"Editing {len(indices)} selected Task(s)...")

        if self.dialog.description == self.STRING_DIFFERENT_VALUES:
            description = False
        else:
            description = self.dialog.description

        if self.dialog.notes == self.STRING_DIFFERENT_VALUES:
            notes = False
        else:
            notes = self.dialog.notes

        if self.dialog.date_due_enabled:
            if self.dialog.date_due == self.STRING_DIFFERENT_VALUES:
                date_due = False
            else:
                date_due = datetime.strptime(self.dialog.date_due, "%d.%m.%Y %H:%M")
        else:
            date_due = None

        try:
            for index in indices:
                self.model.edit_task(index, description, notes, date_due)
                logging.info(f'Task "{description}" at index {index} edited')
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

    def populate_widgets(self) -> None:
        indices = self.table_model.get_selected_source_rows()
        if len(indices) == 0:
            raise IndexError("Editing with no selected Task attempted.")

        selected_tasks = [self.model.task_list[index] for index in indices]
        description_0 = selected_tasks[0].description
        notes_0 = selected_tasks[0].notes
        date_due_0 = selected_tasks[0].date_due

        if all(task.description == description_0 for task in selected_tasks):
            self.dialog.description = description_0
        else:
            self.dialog.description = self.STRING_DIFFERENT_VALUES

        if all(task.notes == notes_0 for task in selected_tasks):
            if notes_0 is None:
                self.dialog.notes = ""
            else:
                self.dialog.notes = notes_0
        else:
            self.dialog.notes = self.STRING_DIFFERENT_VALUES

        if all(task.date_due == date_due_0 for task in selected_tasks):
            if date_due_0 is None:
                special_text = self.STRING_NO_DATE_DUE_SET
            else:
                special_text = ""
            self.dialog.set_date_due(date_due_0, special_text)
        else:
            self.dialog.set_date_due(False, self.STRING_DIFFERENT_VALUES)

    def handle_exception(self) -> None:
        display_text, display_details = handle_exception()  # type: ignore
        self.dialog.display_error(display_text, display_details)
