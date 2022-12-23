from enum import Enum
from typing import Union, Any

from PySide6.QtCore import (
    Qt,
    QMetaObject,
    Slot,
    QModelIndex,
    QPersistentModelIndex,
    QAbstractTableModel,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QCompleter,
    QTableView,
    QHeaderView,
    QSizePolicy,
)

from ftt.ui.state import get_state


# The rough plan:
# QLineEdit generate a signal like textChanged().
# This signal will be send to a second thread which will check for a new query of your database.
# The response will be send to the gui thread to actualize the QCompleter.
# The word list is provided as a QAbstractItemModel which then can be used to update the QCompleter.
#
# Search is possible by using IBKR' API, more details https://interactivebrokers.github.io/tws-api/matching_symbols.html


class SecuritiesModel(QAbstractTableModel):
    class Headers(str, Enum):
        SYMBOL = "Symbol"
        STOCK_EXCHANGE = "Stock Exchange"
        CURRENCY = "Currency"

    def __init__(self, *args, securities=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.securities: list[dict] = securities or []

    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role == Qt.DisplayRole:
            return self.securities[index.row()][
                list(self.Headers)[index.column()].value
            ]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

    def insertRow(self, row, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.securities.insert(row, {i.value: "" for i in self.Headers})
        self.endInsertRows()
        return True

    def setData(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        value: Any,
        role: int = Qt.EditRole,
    ) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        self.securities[index.row()][list(self.Headers)[index.column()].value] = value
        self.dataChanged.emit(index, index, [role])
        return True

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return list(self.Headers)[section].value
        return super().headerData(section, orientation, role)

    def rowCount(self, index=None):
        return len(self.securities)

    def columnCount(self, parent=QModelIndex()):
        return len(self.Headers)

    def removeRows(self, position, rows, index):
        self.beginRemoveRows(index, position, position + rows - 1)
        for i in range(rows):
            del self.securities[position]
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True


class SearchSecurityFormElement(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self.confirm_button = None
        self.search_input = None
        self.model = model
        self._state = get_state()
        self.completer = QCompleter(self.model)

    def createUI(self, dialog: QDialog):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(QLabel("Name"))

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setCompleter(self.completer)
        layout.addWidget(self.search_input)

        self.confirm_button = QPushButton("Add")
        self.confirm_button.setObjectName("confirm_button")
        layout.addWidget(self.confirm_button)

        QMetaObject.connectSlotsByName(self)

        dialog.layout().addWidget(self)

        self._state.signals.selectedPortfolioVersionSecuritiesChanged.connect(
            lambda: self.search_input.clear()
        )
        self._state.signals.addSecurityDialogClosed.connect(
            lambda: self.search_input.clear()
        )

    @Slot()
    def on_search_input_textChanged(self):
        print("text changed: ")

    @Slot()
    def on_confirm_button_clicked(self):
        last = self.model.rowCount()
        self.model.insertRow(last)
        self.model.setData(self.model.index(last, 0), self.search_input.text())
        self.search_input.clear()


class SecuritiesTable(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self._state = get_state()
        self.table = None
        self.model = model

    def createUI(self, dialog: QDialog):
        layout = QHBoxLayout(self)

        self.table = QTableView()
        self.table.setModel(self.model)

        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.table.verticalHeader()
        vertical_header.setVisible(False)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size.setHorizontalStretch(1)
        self.table.setSizePolicy(size)

        layout.addWidget(self.table)

        dialog.layout().addWidget(self)

        self._state.signals.selectedPortfolioVersionSecuritiesChanged.connect(
            lambda: self.model.removeRows(0, self.model.rowCount(), QModelIndex())
        )
        self._state.signals.addSecurityDialogClosed.connect(
            lambda: self.model.removeRows(0, self.model.rowCount(), QModelIndex())
        )


class AddSecuritiesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self._layout = None
        self._state = get_state()
        self.model = SecuritiesModel(
            collection=[], headers=["Symbol", "Stock Exchange", "Currency"]
        )
        self.createUI()

    def createUI(self):
        self.setWindowTitle("Add Securities")
        self.resize(500, 500)
        self._layout = QVBoxLayout(self)

        SearchSecurityFormElement(self.model).createUI(self)
        SecuritiesTable(self.model).createUI(self)

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self._layout.addWidget(buttons)

    def accept(self) -> None:
        # Similarly to PortfolioVersionSecuritiesAddingHandler, we need to
        # load securities information from yfinance
        # 1. in the case of successful retrieving basic information do nothing and wait for "save" button
        # when "save" clicked
        #      upsert a new security,
        #      associate with portfolio version
        #      emit a signal to update the table, and close the dialog
        # 2. in the case of failure,
        #      show a message box with the error under the search input
        #      and leave the dialog open
        # Additionally, keep the "add button" disabled and replace text to "Loading ..."
        self._state.confirm_add_security_dialog()
        super().accept()

    def reject(self) -> None:
        self._state.close_add_security_dialog()
        super().reject()


#
#
# class Ui_AddSecuritiesDialog:
#     def setupUi(self, AddSecuritiesDialog):
#         AddSecuritiesDialog.setObjectName("AddSecuritiesDialog")
#         AddSecuritiesDialog.resize(400, 300)
#         self.verticalLayout = QtWidgets.QVBoxLayout(AddSecuritiesDialog)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.label = QtWidgets.QLabel(AddSecuritiesDialog)
#         self.label.setObjectName("label")
#         self.verticalLayout.addWidget(self.label)
#         self.lineEdit = QtWidgets.QLineEdit(AddSecuritiesDialog)
#         self.lineEdit.setObjectName("lineEdit")
#         self.verticalLayout.addWidget(self.lineEdit)
#         self.buttonBox = QtWidgets.QDialogButtonBox(AddSecuritiesDialog)
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")
#         self.verticalLayout.addWidget(self.buttonBox)
#
#         self.retranslateUi(AddSecuritiesDialog)
#         self.buttonBox.accepted.connect(AddSecuritiesDialog.accept)
#         self.buttonBox.rejected.connect(AddSecuritiesDialog.reject)
#         QtCore.QMetaObject.connectSlotsByName(AddSecuritiesDialog)
#
#     def retranslateUi(self, AddSecuritiesDialog):
#         _translate = QtCore.QCoreApplication.translate
#         AddSecuritiesDialog.setWindowTitle(_translate("AddSecuritiesDialog", "Dialog"))
#         self.label.setText(_translate("AddSecuritiesDialog", "Enter the symbol of the security to add"))
#
#
# class AddSecuritiesDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.ui = Ui_AddSecuritiesDialog()
#         self.ui.setupUi(self)
#         self.ui.buttonBox.accepted.connect(self.accept)
#         self.ui.buttonBox.rejected.connect(self.reject)
#
#     def getSecurities(self):
#         return self.ui.securities.text().split(',')
#
#     @staticmethod
#     def getSecuritiesFromUser(parent=None):
#         dialog = AddSecuritiesDialog(parent)
#         result = dialog.exec_()
#         securities = dialog.getSecurities()
#         return (securities, result == QDialog.Accepted)
