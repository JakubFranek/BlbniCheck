import json
import logging

from src.models.model import Model
from src.presenters.task_dialog_presenter import TaskDialogPresenter
from src.utilities.handle_exception import handle_exception
from src.utilities.json.custom_json_decoder import CustomJSONDecoder
from src.utilities.json.custom_json_encoder import CustomJSONEncoder
from src.views.main_view import MainView
from src.views.view_models.task_table_model import TaskTableModel
from src.views.view_models.task_table_proxy import TaskTableProxy


class MainPresenter:
    def __init__(self, main_view: MainView, model: Model) -> None:
        self.main_view = main_view
        self.model = model

        self.current_file_path: str | None = None

        self.main_view.signal_create_task.connect(lambda: self.create_dialog(False))
        self.main_view.signal_edit_task.connect(lambda: self.create_dialog(True))
        self.main_view.signal_delete_task.connect(self.delete_tasks)
        self.main_view.signal_open.connect(self.load_from_file)
        self.main_view.signal_save.connect(self.save_to_file)
        self.main_view.signal_save_as.connect(lambda: self.save_to_file(True))
        self.main_view.signal_exit.connect(self.close)
        self.main_view.signal_set_tasks_done.connect(
            lambda: self.set_tasks_status(True)
        )
        self.main_view.signal_set_tasks_undone.connect(
            lambda: self.set_tasks_status(False)
        )
        self.main_view.signal_table_selection_changed.connect(
            self.table_selection_changed
        )

        self.model.event_task_added.append(lambda: self.update_unsaved_changes(True))
        self.model.event_task_deleted.append(lambda: self.update_unsaved_changes(True))
        self.model.event_task_edited.append(lambda: self.update_unsaved_changes(True))
        self.model.event_task_list_loaded.append(
            lambda: self.update_unsaved_changes(False)
        )

        self.task_table_proxy = TaskTableProxy()
        self.task_table_model = TaskTableModel(
            self.model, self.main_view.tableView, self.task_table_proxy
        )
        self.task_table_proxy.setSourceModel(self.task_table_model)
        self.main_view.tableView.setModel(self.task_table_proxy)

        self.task_dialog_presenter = TaskDialogPresenter(
            self.model, self.task_table_model
        )

        self.main_view.finalize_setup()
        self.update_unsaved_changes(False)
        self.table_selection_changed()

        logging.info("Showing MainView")
        self.main_view.show()

    def create_dialog(self, edit_mode: bool) -> None:
        self.task_dialog_presenter.create_dialog(edit_mode)

    def delete_tasks(self) -> None:
        try:
            indices = self.task_table_model.get_selected_source_rows()
            if len(indices) >= 1:
                for index in sorted(indices, reverse=True):
                    self.task_table_model.pre_delete_task(index)
                    description = self.model.task_list[index].description
                    self.model.delete_task(index)
                    self.task_table_model.post_delete_task()
                    logging.info(f"Removed Task '{description}' from index {index}")
        except Exception:
            self.handle_exception()

    def set_tasks_status(self, status: bool) -> None:
        try:
            indices = self.task_table_model.get_selected_source_rows()
            if len(indices) >= 1:
                for index in indices:
                    description = self.model.task_list[index].description
                    self.model.set_task_status(index, status)
                    logging.info(
                        f"Set Task '{description}' as \"{'Done' if status else 'Undone'}\""
                    )
                self.main_view.tableView.viewport().update()
        except Exception:
            self.handle_exception()

    def save_to_file(self, save_as: bool = False) -> None:
        logging.info("Saving to JSON file...")
        try:
            if save_as is True or self.current_file_path is None:
                file_path, _ = self.main_view.get_save_path()
                if file_path != "":
                    self.current_file_path = file_path

            if isinstance(self.current_file_path, str):
                with open(self.current_file_path, "w") as file:
                    json.dump(self.model.task_list, file, cls=CustomJSONEncoder)
                    self.update_unsaved_changes(False)
                    self.main_view.statusBar().showMessage(
                        f"File saved ({self.current_file_path})", 2000
                    )
                    logging.info(f"File saved to {self.current_file_path}")
            else:
                logging.info("Invalid or no file path received, file saving cancelled")
        except Exception:
            self.handle_exception()

    def load_from_file(self) -> None:
        logging.info("Loading from JSON file...")
        try:
            file_path, _ = self.main_view.get_open_path()
            if file_path != "":
                self.current_file_path = file_path
                with open(file_path, "r") as file:
                    list_tasks = json.load(file, cls=CustomJSONDecoder)
                    length = len(list_tasks)
                    self.task_table_model.pre_new_list()
                    self.model.load_task_list(list_tasks)
                    self.task_table_model.post_new_list()
                    self.main_view.statusBar().showMessage(
                        f"File loaded ({self.current_file_path})", 2000
                    )
                    logging.info(
                        f"JSON file containing {length} Task(s) loaded from {file_path}"
                    )
            else:
                logging.info("Invalid or no file path received, file load cancelled")
        except Exception:
            self.handle_exception()

    def close(self) -> None:
        logging.info("Close called...")
        if self.unsaved_changes is True:
            reply = self.main_view.ask_save_before_close()
            if reply is True:
                self.save_to_file()
                if self.unsaved_changes is False:
                    logging.info("Closing after saving")
                    self.main_view.close()
                else:
                    logging.info("Close cancelled")
            elif reply is False:
                logging.info("Closing without saving")
                self.main_view.close()
            else:
                logging.info("Close cancelled")
        else:
            logging.info("Closing")
            self.main_view.close()

    def update_unsaved_changes(self, unsaved_changes: bool) -> None:
        self.unsaved_changes = unsaved_changes
        no_of_tasks = len(self.model.task_list)
        enable_save_as = no_of_tasks > 0
        self.main_view.set_save_status(
            self.current_file_path, self.unsaved_changes, enable_save_as
        )

    def table_selection_changed(self) -> None:
        indices = self.task_table_model.get_selected_source_rows()
        if len(indices) > 0:
            self.main_view.update_task_actions(True)
        else:
            self.main_view.update_task_actions(False)

    def handle_exception(self) -> None:
        display_text, display_details = handle_exception()  # type: ignore
        self.main_view.display_error(display_text, display_details)
