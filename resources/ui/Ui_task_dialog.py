# Form implementation generated from reading ui file 'd:\Coding\BlbniCheck\resources\ui\task_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TaskDialog(object):
    def setupUi(self, TaskDialog):
        TaskDialog.setObjectName("TaskDialog")
        TaskDialog.resize(322, 161)
        TaskDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(TaskDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelDescription = QtWidgets.QLabel(TaskDialog)
        self.labelDescription.setObjectName("labelDescription")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelDescription)
        self.lineEditDescription = QtWidgets.QLineEdit(TaskDialog)
        self.lineEditDescription.setObjectName("lineEditDescription")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditDescription)
        self.labelNotes = QtWidgets.QLabel(TaskDialog)
        self.labelNotes.setObjectName("labelNotes")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelNotes)
        self.labelDueDate = QtWidgets.QLabel(TaskDialog)
        self.labelDueDate.setObjectName("labelDueDate")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelDueDate)
        self.dateTimeEditDueDate = QtWidgets.QDateTimeEdit(TaskDialog)
        self.dateTimeEditDueDate.setCalendarPopup(True)
        self.dateTimeEditDueDate.setObjectName("dateTimeEditDueDate")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.dateTimeEditDueDate)
        self.plainTextEditNotes = QtWidgets.QPlainTextEdit(TaskDialog)
        self.plainTextEditNotes.setMinimumSize(QtCore.QSize(0, 50))
        self.plainTextEditNotes.setTabChangesFocus(True)
        self.plainTextEditNotes.setObjectName("plainTextEditNotes")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.plainTextEditNotes)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(TaskDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TaskDialog)
        self.buttonBox.accepted.connect(TaskDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(TaskDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TaskDialog)
        TaskDialog.setTabOrder(self.lineEditDescription, self.plainTextEditNotes)
        TaskDialog.setTabOrder(self.plainTextEditNotes, self.dateTimeEditDueDate)

    def retranslateUi(self, TaskDialog):
        _translate = QtCore.QCoreApplication.translate
        TaskDialog.setWindowTitle(_translate("TaskDialog", "Create a new Task"))
        self.labelDescription.setText(_translate("TaskDialog", "Description"))
        self.lineEditDescription.setPlaceholderText(_translate("TaskDialog", "Enter the Task title"))
        self.labelNotes.setText(_translate("TaskDialog", "Notes"))
        self.labelDueDate.setText(_translate("TaskDialog", "Due Date"))
        self.plainTextEditNotes.setPlaceholderText(_translate("TaskDialog", "Enter optional details"))