import copy

from PySide6.QtGui import QPalette
from PySide6.QtSql import QSqlRelationalDelegate
from PySide6.QtWidgets import QTableView


class TickerDelegate(QSqlRelationalDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        opt = copy.copy(option)
        opt.rect = option.rect.adjusted(0, 0, -1, -1)
        QSqlRelationalDelegate.paint(self, painter, opt, index)

        pen = painter.pen()
        painter.setPen(option.palette.color(QPalette.Mid))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.setPen(pen)

    def createEditor(self, parent, option, index):
        return QSqlRelationalDelegate.createEditor(self, parent, option, index)

    def editorEvent(self, event, model, option, index):
        return False


class BookTable(QTableView):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
