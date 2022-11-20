import os

from PyQt6.QtCore import QDir, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from resources.ui.Ui_main_window import Ui_MainWindow


class MainView(QMainWindow, Ui_MainWindow):
    signal_create_task = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.full_setup()

    def display_error(
        self,
        text: str,
        exc_details: str,
        title: str = "Error!",
    ) -> None:
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setDetailedText(exc_details)
        message_box.setWindowIcon(QIcon("icons_24:cross.png"))

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
