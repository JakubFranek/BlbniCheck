from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class IconDelegate(QStyledItemDelegate):
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        option.decorationSize = option.rect.size()
