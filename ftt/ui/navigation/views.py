from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QListView, QItemDelegate, QPushButton


class NavigationDelegate(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        if not self.parent().indexWidget(index):
            button = QPushButton(index.data(), self.parent())
            button.setMinimumSize(QtCore.QSize(170, 30))
            button.setMaximumSize(QtCore.QSize(170, 30))
            button.clicked.connect(lambda: self.parent().portfolio_selected(index))
            self.parent().setIndexWidget(index, button)


class NavigationView(QListView):
    def __init__(self, model, parent=None, delegate=NavigationDelegate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.view = delegate(self)
        # self.setItemDelegate(self.view)

        self.setWordWrap(True)
        self.setUniformItemSizes(True)
        self.setSpacing(10)
        self.setFixedWidth(200)
        self.setStyleSheet("QListView {background-color: #f5f5f5; border: none;}")

        # self.selectionModel().currentChanged.connect(self.on_current_changed)

    def init_ui(self):
        pass

    def portfolio_selected(self, index):
        print("index: ", index)
        self.select(index)

    def selectionChanged(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection) -> None:
        print("selected: ", selected, deselected)
        super().selectionChanged(selected, deselected)

    def select(self, index):
        print("index: ", index)
        sm = self.selectionModel()
        sm.setSelection(index, QtCore.QItemSelectionModel.SelectionFlag.Select)

    def on_current_changed(self, current, previous):
        print("current: ", current, previous)