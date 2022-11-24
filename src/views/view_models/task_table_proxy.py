import logging
from datetime import datetime

from PyQt6.QtCore import QModelIndex, QSortFilterProxyModel, Qt


class TaskTableProxy(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        column_left = left.column()
        column_right = right.column()

        if column_left != column_right:
            raise ValueError("Column indexes do not match.")

        if column_left != 0:
            data_left: str = self.sourceModel().data(left, Qt.ItemDataRole.DisplayRole)
            data_right: str = self.sourceModel().data(
                right, Qt.ItemDataRole.DisplayRole
            )
        else:
            data_left: str = self.sourceModel().data(left, Qt.ItemDataRole.DisplayRole)
            data_right: str = self.sourceModel().data(
                right, Qt.ItemDataRole.DisplayRole
            )

        if data_left and data_right:
            if column_left == 0:
                return data_left < data_right
            if column_left == 1:
                return str(data_left) < str(data_right)
            elif column_left == 2:
                datetime_left = datetime.strptime(data_left, "%d/%m/%Y %H:%M")
                datetime_right = datetime.strptime(data_right, "%d/%m/%Y %H:%M")
                return datetime_left < datetime_right
            else:
                logging.warning(f"Incorrect column index accessed ({column_left})")
                return False
        elif data_left or data_right:
            return bool(data_left)
        else:
            logging.warning("Data of 'falsy' Value compared during sorting")
            return False
