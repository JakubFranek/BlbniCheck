from PyQt6.QtWidgets import QTableView, QWidget
from pytestqt.modeltest import ModelTester
from pytestqt.qtbot import QtBot

from src.models.model import Model
from src.views.view_models.task_table_model import TaskTableModel


def test_task_table_model(qtbot: QtBot, qtmodeltester: ModelTester) -> None:
    parent = QWidget()
    qtbot.add_widget(parent)
    table_view = QTableView(parent)
    domain_model = Model()
    domain_model.add_task("Test", "notes", None)
    domain_model.add_task("abcd", "", None)
    domain_model.add_task("XXX", "notes", None)
    model = TaskTableModel(domain_model, table_view)

    qtmodeltester.check(model)
