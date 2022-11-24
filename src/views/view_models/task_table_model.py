from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTableView

from src.models.model import Model


class TaskTableModel(QAbstractTableModel):

    headers = ("Status", "Description", "Date Due")

    def __init__(
        self,
        model: Model,
        view: QTableView,
        proxy: QSortFilterProxyModel | None = None,
    ) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.proxy = proxy

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = ...) -> Any:
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            task = self.model.task_list[index.row()]

            if column == 0:
                return task.done
            elif column == 1:
                return task.description
            elif column == 2:
                if task.date_due is not None:
                    return task.date_due.strftime("%d/%m/%Y %H:%M")
                else:
                    return ""
            else:
                raise ValueError(
                    f"Column index must be less than or equal to 2 (is {column})."
                )
        elif role == Qt.ItemDataRole.DecorationRole:
            task = self.model.task_list[index.row()]
            if column == 0:
                if task.done is True:
                    return QIcon("icons_16:tick-button.png")
                else:
                    return QIcon("icons_16:cross-button.png")
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            elif column == 1:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            elif column == 2:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                raise ValueError(
                    f"Column index must be less than or equal to 2 (is {column})."
                )

    def rowCount(self, index: QModelIndex = ...) -> int:  # noqa:U100
        return len(self.model.task_list)

    def columnCount(self, index: QModelIndex = ...) -> int:  # noqa:U100
        return 3

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
        self.view.sortByColumn(2, Qt.SortOrder.AscendingOrder)
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
