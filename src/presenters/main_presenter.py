import logging

from src.models.model import Model
from src.presenters.task_dialog_presenter import TaskDialogPresenter
from src.views.main_view import MainView
from src.views.view_models.task_table_model import TaskTableModel


class MainPresenter:
    def __init__(self, main_view: MainView, model: Model) -> None:
        self.main_view = main_view
        self.model = model

        self.main_view.signal_create_task.connect(self.create_task)

        self.task_table_model = TaskTableModel(self.model, self.main_view.tableView)
        self.main_view.tableView.setModel(self.task_table_model)

        self.task_dialog_presenter = TaskDialogPresenter(
            self.model, self.task_table_model
        )

        logging.info("Showing MainView")
        self.main_view.show()

    def create_task(self) -> None:
        self.task_dialog_presenter.create_dialog()
