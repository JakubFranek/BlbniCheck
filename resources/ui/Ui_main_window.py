# Form implementation generated from reading ui file 'd:\Coding\BlbniCheck\resources\ui\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        MainWindow.setMinimumSize(QtCore.QSize(300, 300))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedKingdom))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setStatusTip("")
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(True)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setStretchLastSection(False)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionCreate_Task = QtGui.QAction(MainWindow)
        self.actionCreate_Task.setObjectName("actionCreate_Task")
        self.actionEdit_Task = QtGui.QAction(MainWindow)
        self.actionEdit_Task.setObjectName("actionEdit_Task")
        self.actionDelete_Task = QtGui.QAction(MainWindow)
        self.actionDelete_Task.setObjectName("actionDelete_Task")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSet_as_Done = QtGui.QAction(MainWindow)
        self.actionSet_as_Done.setObjectName("actionSet_as_Done")
        self.actionSet_as_Undone = QtGui.QAction(MainWindow)
        self.actionSet_as_Undone.setObjectName("actionSet_as_Undone")
        self.actionShow_Done_Tasks = QtGui.QAction(MainWindow)
        self.actionShow_Done_Tasks.setObjectName("actionShow_Done_Tasks")
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_As)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreate_Task)
        self.toolBar.addAction(self.actionEdit_Task)
        self.toolBar.addAction(self.actionDelete_Task)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSet_as_Done)
        self.toolBar.addAction(self.actionSet_as_Undone)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionShow_Done_Tasks)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BlbniCheck"))
        self.statusbar.setStatusTip(_translate("MainWindow", "This is me, the status bar!"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionCreate_Task.setText(_translate("MainWindow", "Create Task"))
        self.actionCreate_Task.setToolTip(_translate("MainWindow", "Create a new Task"))
        self.actionCreate_Task.setStatusTip(_translate("MainWindow", "Create a new Task"))
        self.actionCreate_Task.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionEdit_Task.setText(_translate("MainWindow", "Edit Task(s)"))
        self.actionEdit_Task.setToolTip(_translate("MainWindow", "Edit selected Task(s)"))
        self.actionEdit_Task.setStatusTip(_translate("MainWindow", "Edit selected Task(s)"))
        self.actionEdit_Task.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionDelete_Task.setText(_translate("MainWindow", "Delete Task(s)"))
        self.actionDelete_Task.setToolTip(_translate("MainWindow", "Delete selected Task(s)"))
        self.actionDelete_Task.setStatusTip(_translate("MainWindow", "Delete selected Task(s)"))
        self.actionDelete_Task.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save to current file"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save to current file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a file"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Open a file"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionSave_As.setToolTip(_translate("MainWindow", "Save to a file of your choosing"))
        self.actionSave_As.setStatusTip(_translate("MainWindow", "Save to a file of your choosing"))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionSet_as_Done.setText(_translate("MainWindow", "Set as Done"))
        self.actionSet_as_Done.setToolTip(_translate("MainWindow", "Set selected Task(s) as Done"))
        self.actionSet_as_Done.setStatusTip(_translate("MainWindow", "Set selected Task(s) as Done"))
        self.actionSet_as_Undone.setText(_translate("MainWindow", "Set as Undone"))
        self.actionSet_as_Undone.setToolTip(_translate("MainWindow", "Set selected Task(s) as Undone"))
        self.actionSet_as_Undone.setStatusTip(_translate("MainWindow", "Set selected Task(s) as Undone"))
        self.actionShow_Done_Tasks.setText(_translate("MainWindow", "Show Done Tasks"))
        self.actionShow_Done_Tasks.setToolTip(_translate("MainWindow", "Check to show Done Tasks"))
        self.actionShow_Done_Tasks.setStatusTip(_translate("MainWindow", "Check to show Done Tasks"))
