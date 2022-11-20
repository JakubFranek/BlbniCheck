from PyQt6.QtCore import QDateTime, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox

from resources.ui.Ui_task_dialog import Ui_TaskDialog


class TaskDialog(QDialog, Ui_TaskDialog):
    signal_ok = pyqtSignal()
    signal_apply = pyqtSignal()
    signal_cancel = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("icons_24:plus.png"))
        self.dateTimeEditDueDate.setDateTime(QDateTime.currentDateTime())
        self.buttonBox.clicked.connect(self.handleButtonBoxClick)

    @property
    def description(self) -> str:
        return self.lineEditDescription.text()

    @property
    def notes(self) -> str:
        return self.plainTextEditNotes.toPlainText()

    @property
    def date_due(self) -> str:
        return self.dateTimeEditDueDate.dateTime().toString("dd.MM.yyyy hh:mm")

    def handleButtonBoxClick(self, button: QAbstractButton) -> None:
        role = self.buttonBox.buttonRole(button)
        if role == QDialogButtonBox.ButtonRole.AcceptRole:
            self.signal_ok.emit()
        elif role == QDialogButtonBox.ButtonRole.ApplyRole:
            self.signal_apply.emit()
        elif role == QDialogButtonBox.ButtonRole.RejectRole:
            self.signal_cancel.emit()
        else:
            raise ValueError("Unknown role of the clicked button in the ButtonBox")
