from datetime import datetime
from typing import Literal

from PyQt6.QtCore import QDateTime, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QIcon
from PyQt6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox, QMessageBox

from resources.ui.Ui_task_dialog import Ui_TaskDialog


class TaskDialog(QDialog, Ui_TaskDialog):
    signal_ok = pyqtSignal()
    signal_apply = pyqtSignal()
    signal_cancel = pyqtSignal()
    signal_date_due_toggle = pyqtSignal()

    STRING_DIFFERENT_VALUES = "Keep current values"
    TEXT_COLOR_GRAY = "#808080"

    def __init__(self, edit_mode: bool) -> None:
        super().__init__()
        self.setupUi(self)

        if edit_mode is True:
            self.setWindowIcon(QIcon("icons_24:pencil.png"))
            self.setWindowTitle("Edit selected Task(s)")
        else:
            self.setWindowIcon(QIcon("icons_24:plus.png"))
            self.setWindowTitle("Create a new Task")

        self.dateTimeEditDueDate.setDateTime(QDateTime.currentDateTime())
        self.buttonBox.clicked.connect(self.handleButtonBoxClick)
        self.checkBox.stateChanged.connect(lambda: self.signal_date_due_toggle.emit())

        self.lineEditDescription.textChanged.connect(self.description_edited)
        self.plainTextEditNotes.textChanged.connect(self.notes_edited)

        self.checkBox.setChecked(False)
        self.dateTimeEditDueDate.setEnabled(False)

    @property
    def description(self) -> str:
        return self.lineEditDescription.text()

    @description.setter
    def description(self, value: str) -> None:
        self.lineEditDescription.setText(value)

    @property
    def notes(self) -> str:
        return self.plainTextEditNotes.toPlainText()

    @notes.setter
    def notes(self, value: str) -> None:
        self.plainTextEditNotes.setPlainText(value)

    @property
    def date_due_enabled(self) -> bool:
        return self.checkBox.isChecked()

    @property
    def date_due(self) -> str:
        if (
            self.dateTimeEditDueDate.minimumDateTime()
            == self.dateTimeEditDueDate.dateTime()
        ):
            return self.dateTimeEditDueDate.specialValueText()
        else:
            return self.dateTimeEditDueDate.dateTime().toString("dd.MM.yyyy hh:mm")

    def set_date_due(
        self, value: datetime | None | Literal[False], special_text: str = ""
    ) -> None:
        if value is False:
            self.dateTimeEditDueDate.setSpecialValueText(special_text)
            self.dateTimeEditDueDate.setDateTime(
                self.dateTimeEditDueDate.minimumDateTime()
            )
            self.checkBox.setChecked(True)
        elif isinstance(value, datetime):
            self.dateTimeEditDueDate.setDateTime(value)
            self.checkBox.setChecked(True)
        elif value is None:
            self.dateTimeEditDueDate.setSpecialValueText(special_text)
            self.dateTimeEditDueDate.setDateTime(
                self.dateTimeEditDueDate.minimumDateTime()
            )
            self.checkBox.setChecked(False)
        else:
            raise ValueError("Invalid date_due setter input.")

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

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.signal_cancel.emit()

    def description_edited(self) -> None:
        current_text = self.lineEditDescription.text()
        if current_text == self.STRING_DIFFERENT_VALUES:
            self.lineEditDescription.setStyleSheet(f"color: {self.TEXT_COLOR_GRAY}")
        else:
            self.lineEditDescription.setStyleSheet("")

    def notes_edited(self) -> None:
        current_text = self.plainTextEditNotes.toPlainText()
        if current_text == self.STRING_DIFFERENT_VALUES:
            self.plainTextEditNotes.setStyleSheet(f"color: {self.TEXT_COLOR_GRAY}")
        else:
            self.plainTextEditNotes.setStyleSheet("")

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
