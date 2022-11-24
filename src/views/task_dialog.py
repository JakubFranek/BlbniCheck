from PyQt6.QtCore import QDateTime, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox, QMessageBox

from resources.ui.Ui_task_dialog import Ui_TaskDialog


class TaskDialog(QDialog, Ui_TaskDialog):
    signal_ok = pyqtSignal()
    signal_apply = pyqtSignal()
    signal_cancel = pyqtSignal()
    signal_date_due_toggle = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("icons_24:plus.png"))
        self.dateTimeEditDueDate.setDateTime(QDateTime.currentDateTime())
        self.buttonBox.clicked.connect(self.handleButtonBoxClick)
        self.checkBox.stateChanged.connect(lambda: self.signal_date_due_toggle.emit())

        self.checkBox.setChecked(False)
        self.dateTimeEditDueDate.setEnabled(False)

    @property
    def description(self) -> str:
        return self.lineEditDescription.text()

    @property
    def notes(self) -> str:
        return self.plainTextEditNotes.toPlainText()

    @property
    def date_due_enabled(self) -> bool:
        return self.checkBox.isChecked()

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
