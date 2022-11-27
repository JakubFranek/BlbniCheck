import os

from PyQt6.QtCore import QDir, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QContextMenuEvent, QCursor, QIcon
from PyQt6.QtWidgets import QFileDialog, QHeaderView, QMainWindow, QMenu, QMessageBox

from resources.ui.Ui_main_window import Ui_MainWindow
from src.views.utilities.icon_delegate import IconDelegate


class MainView(QMainWindow, Ui_MainWindow):
    signal_create_task = pyqtSignal()
    signal_delete_task = pyqtSignal()
    signal_save = pyqtSignal()
    signal_save_as = pyqtSignal()
    signal_open = pyqtSignal()
    signal_exit = pyqtSignal()
    signal_edit_task = pyqtSignal()
    signal_table_selection_changed = pyqtSignal()
    signal_set_tasks_done = pyqtSignal()
    signal_set_tasks_undone = pyqtSignal()
    signal_show_done_tasks_changed = pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.initial_setup()

    def get_save_path(self) -> tuple[str, str]:
        return QFileDialog.getSaveFileName(self, filter="JSON file (*.json)")

    def get_open_path(self) -> tuple[str, str]:
        return QFileDialog.getOpenFileName(self, filter="JSON file (*.json)")

    def ask_save_before_close(self) -> bool | None:
        reply = QMessageBox.question(
            self,
            "Save changes before quitting?",
            "There have been changes to the data which are not yet saved.\nDo you want to save them before quitting?",
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel
            ),
            QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Yes:
            return True
        elif reply == QMessageBox.StandardButton.No:
            return False
        else:
            return None

    def set_save_status(
        self, current_file_path: str | None, unsaved_changes: bool, enable_save_as: bool
    ) -> None:
        if unsaved_changes is True:
            self.actionSave.setIcon(QIcon("icons_16:disk--exclamation.png"))
            star_str = "*"
        else:
            self.actionSave.setIcon(QIcon("icons_16:disk.png"))
            star_str = ""

        if current_file_path is None:
            self.actionSave.setEnabled(False)
            self.setWindowTitle("Blbnicheck")
        else:
            self.actionSave.setEnabled(True)
            self.setWindowTitle("Blbnicheck - " + current_file_path + star_str)

        self.actionSave_As.setEnabled(enable_save_as)

    def update_task_actions(self, selected: bool) -> None:
        self.actionEdit_Task.setEnabled(selected)
        self.actionDelete_Task.setEnabled(selected)
        self.actionSet_as_Done.setEnabled(selected)
        self.actionSet_as_Undone.setEnabled(selected)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:  # noqa: U100
        self.menu = QMenu(self)
        self.menu.addAction(self.actionSet_as_Done)
        self.menu.addAction(self.actionSet_as_Undone)
        self.menu.addSeparator()
        self.menu.addAction(self.actionDelete_Task)
        self.menu.addAction(self.actionEdit_Task)
        self.menu.popup(QCursor.pos())

    def closeEvent(self, event: QCloseEvent) -> None:
        self.signal_exit.emit()
        event.ignore()

    def initial_setup(self) -> None:
        QDir.addSearchPath(
            "icons_24",
            os.path.join(QDir.currentPath(), "resources/icons/bonus/icons-24"),
        )
        QDir.addSearchPath(
            "icons_16",
            os.path.join(QDir.currentPath(), "resources/icons/icons"),
        )
        QDir.addSearchPath(
            "icons_custom",
            os.path.join(QDir.currentPath(), "resources/icons/icons-custom"),
        )

        self.setupUi(self)

        self.setWindowIcon(QIcon("icons_custom:tick.ico"))
        self.actionOpen.setIcon(QIcon("icons_16:folder-open.png"))
        self.actionSave.setIcon(QIcon("icons_16:disk.png"))
        self.actionSave_As.setIcon(QIcon("icons_16:disks.png"))
        self.actionCreate_Task.setIcon(QIcon("icons_16:plus.png"))
        self.actionEdit_Task.setIcon(QIcon("icons_16:pencil.png"))
        self.actionDelete_Task.setIcon(QIcon("icons_16:minus.png"))
        self.actionSet_as_Done.setIcon(QIcon("icons_16:tick-button.png"))
        self.actionSet_as_Undone.setIcon(QIcon("icons_16:cross-button.png"))
        self.actionShow_Done_Tasks.setIcon(QIcon("icons_custom:eye-tick.png"))

        self.actionShow_Done_Tasks.setCheckable(True)

        self.actionCreate_Task.triggered.connect(lambda: self.signal_create_task.emit())
        self.actionSave.triggered.connect(lambda: self.signal_save.emit())
        self.actionSave_As.triggered.connect(lambda: self.signal_save_as.emit())
        self.actionOpen.triggered.connect(lambda: self.signal_open.emit())
        self.actionDelete_Task.triggered.connect(lambda: self.signal_delete_task.emit())
        self.actionEdit_Task.triggered.connect(lambda: self.signal_edit_task.emit())
        self.actionSet_as_Done.triggered.connect(
            lambda: self.signal_set_tasks_done.emit()
        )
        self.actionSet_as_Undone.triggered.connect(
            lambda: self.signal_set_tasks_undone.emit()
        )
        self.actionShow_Done_Tasks.triggered.connect(
            lambda: self.signal_show_done_tasks_changed.emit(
                self.actionShow_Done_Tasks.isChecked()
            )
        )

        self.tableView.doubleClicked.connect(lambda: self.signal_edit_task.emit())

        icon_delegate = IconDelegate(self.tableView)
        self.tableView.setItemDelegate(icon_delegate)

    def finalize_setup(self) -> None:
        self.tableView.selectionModel().selectionChanged.connect(
            lambda: self.signal_table_selection_changed.emit()
        )

        """ For some reason the lines below cause the program to crash on startup
        without error message if placed in initial_setup() """
        self.tableView.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.tableView.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

    def display_error(
        self,
        text: str,
        exc_details: str,
        critical: bool = False,
        title: str = "Error!",
    ) -> None:
        message_box = QMessageBox()

        if critical is True:
            message_box.setIcon(QMessageBox.Icon.Critical)
            message_box.setWindowIcon(QIcon("icons_24:cross.png"))
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)
            message_box.setWindowIcon(QIcon("icons_24:exclamation.png"))

        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setDetailedText(exc_details)

        message_box.exec()
