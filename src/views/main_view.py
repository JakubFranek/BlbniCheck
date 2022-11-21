import os

from PyQt6.QtCore import QDir, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from resources.ui.Ui_main_window import Ui_MainWindow


class MainView(QMainWindow, Ui_MainWindow):
    signal_create_task = pyqtSignal()
    signal_save = pyqtSignal()
    signal_save_as = pyqtSignal()
    signal_open = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.full_setup()

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

    def full_setup(self) -> None:
        QDir.addSearchPath(
            "icons_24",
            os.path.join(QDir.currentPath(), "resources/icons/bonus/icons-24"),
        )
        QDir.addSearchPath(
            "icons_16",
            os.path.join(QDir.currentPath(), "resources/icons/icons"),
        )

        self.setupUi(self)

        self.setWindowIcon(QIcon("icons_24:tick.png"))
        self.actionOpen.setIcon(QIcon("icons_16:folder-open.png"))
        self.actionSave.setIcon(QIcon("icons_16:disk.png"))
        self.actionSave_As.setIcon(QIcon("icons_16:disks.png"))
        self.actionCreate_Task.setIcon(QIcon("icons_16:plus.png"))
        self.actionEdit_Task.setIcon(QIcon("icons_16:pencil.png"))
        self.actionDelete_Task.setIcon(QIcon("icons_16:minus.png"))

        self.actionCreate_Task.triggered.connect(lambda: self.signal_create_task.emit())
        self.actionSave.triggered.connect(lambda: self.signal_save.emit())
        self.actionSave_As.triggered.connect(lambda: self.signal_save_as.emit())
        self.actionOpen.triggered.connect(lambda: self.signal_open.emit())

    def get_save_path(self) -> tuple[str, str]:
        return QFileDialog.getSaveFileName(self, filter="JSON file (*.json)")

    def get_open_path(self) -> tuple[str, str]:
        return QFileDialog.getOpenFileName(self, filter="JSON file (*.json)")

    def ask_save_before_exit(self) -> bool | None:
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
