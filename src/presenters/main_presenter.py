import json
import logging

from src.models.model import Model
from src.presenters.task_dialog_presenter import TaskDialogPresenter
from src.utilities.handle_exception import handle_exception
from src.utilities.json.custom_json_decoder import CustomJSONDecoder
from src.utilities.json.custom_json_encoder import CustomJSONEncoder
from src.views.main_view import MainView
from src.views.view_models.task_table_model import TaskTableModel


class MainPresenter:
    def __init__(self, main_view: MainView, model: Model) -> None:
        self.main_view = main_view
        self.model = model

        self.current_file_path: str | None = None

        self.main_view.signal_create_task.connect(self.create_task)
        self.main_view.signal_open.connect(self.load_from_file)
        self.main_view.signal_save.connect(self.save_to_file)
        self.main_view.signal_save_as.connect(lambda: self.save_to_file(True))

        self.task_table_model = TaskTableModel(self.model, self.main_view.tableView)
        self.main_view.tableView.setModel(self.task_table_model)

        self.task_dialog_presenter = TaskDialogPresenter(
            self.model, self.task_table_model
        )

        logging.info("Showing MainView")
        self.main_view.show()

    def create_task(self) -> None:
        self.task_dialog_presenter.create_dialog()

    def save_to_file(self, save_as: bool = False) -> None:
        logging.info("Saving to JSON file")
        try:
            if save_as is True or self.current_file_path is None:
                file_path, _ = self.main_view.get_save_path()
                if file_path != "":
                    self.current_file_path = file_path

            if isinstance(self.current_file_path, str):
                with open(self.current_file_path, "w") as file:
                    json.dump(self.model.task_list, file, cls=CustomJSONEncoder)
                    # self.update_unsaved_changes(False)
                    logging.info(f"File saved to {self.current_file_path=}")
            else:
                logging.info("Invalid or no file path received, file saving cancelled")
        except Exception as exception:
            self.handle_exception(exception)

    def load_from_file(self) -> None:
        logging.info("Loading from JSON file")
        try:
            file_path, _ = self.main_view.get_open_path()
            if file_path != "":
                with open(file_path, "r") as file:
                    list_tasks = json.load(file, cls=CustomJSONDecoder)
                    self.task_table_model.pre_new_list()
                    self.model.load_task_list(list_tasks)
                    self.task_table_model.post_new_list()
                    # self.update_unsaved_changes(False)
                    logging.info(f"JSON file loaded from {file_path=}")
            else:
                logging.info("Invalid or no file path received, file load cancelled")
        except Exception as exception:
            self.handle_exception(exception)

    def handle_exception(self, exception: Exception) -> None:
        display_text, display_details = handle_exception(exception)  # type: ignore
        self.main_view.display_error(display_text, display_details)
