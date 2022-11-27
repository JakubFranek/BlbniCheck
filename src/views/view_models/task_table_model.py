from datetime import datetime
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt
from PyQt6.QtGui import QColor, QColorConstants, QIcon
from PyQt6.QtWidgets import QTableView

import src.views.constants as view_constants
from src.models.model import Model


class TaskTableModel(QAbstractTableModel):

    headers = ("Status", "Description", "Date Due")

    def __init__(
        self,
        model: Model,
        view: QTableView,
        proxy: QSortFilterProxyModel | None = None,
        show_done_tasks: bool = True,
    ) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.proxy = proxy
        self.show_done_tasks = show_done_tasks

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = ...) -> Any:
        column = index.column()
        if self.show_done_tasks is True:
            task = self.model.task_list[index.row()]
        else:
            filtered_list = [
                task for task in self.model.task_list if task.done is False
            ]
            task = filtered_list[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if column == view_constants.COLUMN_STATUS:
                return task.done
            elif column == view_constants.COLUMN_DESCRIPTION:
                return task.description
            elif column == view_constants.COLUMN_DATE_DUE:
                if task.date_due is not None:
                    return task.date_due.strftime("%d/%m/%Y %H:%M")
                else:
                    return ""
        elif role == Qt.ItemDataRole.DecorationRole:
            if column == view_constants.COLUMN_STATUS:
                if task.done is True:
                    return QIcon("icons_16:tick-button.png")
                else:
                    return QIcon("icons_16:cross-button.png")
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column == view_constants.COLUMN_STATUS:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            elif column == view_constants.COLUMN_DESCRIPTION:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            elif column == view_constants.COLUMN_DATE_DUE:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.ForegroundRole:
            if column == view_constants.COLUMN_DESCRIPTION:
                if task.done is True:
                    return QColor(QColorConstants.Gray)
            elif column == view_constants.COLUMN_DATE_DUE:
                if task.done is True:
                    return QColor(QColorConstants.Gray)
                else:
                    date_due = task.date_due
                    if date_due and task.done is not True and date_due < datetime.now():
                        return QColor(QColorConstants.Red)
        elif role == Qt.ItemDataRole.ToolTipRole:
            task_notes = task.notes
            if task_notes is not False:
                return task_notes

    def rowCount(self, index: QModelIndex = ...) -> int:  # noqa:U100
        if index.isValid():
            return 0
        else:
            if self.show_done_tasks is True:
                return len(self.model.task_list)
            else:
                return sum(task.done is False for task in self.model.task_list)

    def columnCount(self, index: QModelIndex = ...) -> int:  # noqa:U100
        if index.isValid():
            return 0
        else:
            return view_constants.COLUMN_COUNT

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = ...
    ) -> str | int | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return TaskTableModel.headers[section]
            else:
                return str(section)

    def pre_add(self) -> None:
        if self.proxy is not None:
            self.proxy.setDynamicSortFilter(False)
        self.view.setSortingEnabled(False)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())

    def post_add(self) -> None:
        self.endInsertRows()
        self.view.setSortingEnabled(True)
        if self.proxy is not None:
            self.proxy.setDynamicSortFilter(True)

    def pre_new_list(self) -> None:
        self.view.setSortingEnabled(False)
        self.beginResetModel()

    def post_new_list(self) -> None:
        self.endResetModel()
        self.view.sortByColumn(
            view_constants.COLUMN_DATE_DUE, Qt.SortOrder.AscendingOrder
        )
        self.view.setSortingEnabled(True)

    def pre_reset_model(self) -> None:
        self.view.setSortingEnabled(False)
        self.beginResetModel()

    def post_reset_model(self) -> None:
        self.endResetModel()
        self.view.setSortingEnabled(True)

    def pre_delete_task(self, row: int) -> None:
        self.beginRemoveRows(QModelIndex(), row, row)

    def post_delete_task(self) -> None:
        self.endRemoveRows()

    def get_selected_source_rows(self) -> set[int]:
        indexes: list[QModelIndex] = self.view.selectedIndexes()
        if self.proxy is not None:
            return {self.proxy.mapToSource(index).row() for index in indexes}
        else:
            return {index.row() for index in indexes}
