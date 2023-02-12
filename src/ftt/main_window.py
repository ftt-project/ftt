from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlRelationalTableModel, QSqlTableModel
from PySide6.QtWidgets import QDataWidgetMapper, QMainWindow, QApplication, QStyleFactory, \
    QGroupBox, QFormLayout, QLineEdit, QVBoxLayout, QDialogButtonBox

from ftt.book_table import TickerDelegate, BookTable


class AddTickerWidget(QGroupBox):
    on_create = Signal()
    on_reject = Signal()

    def __init__(self):
        super().__init__()
        self.setTitle("Add Ticker")
        self.setLayout(QFormLayout())

        symbol_edit = QLineEdit()
        symbol_edit.setObjectName("symbol")
        self.layout().addRow("Symbol", symbol_edit)

        exchange_edit = QLineEdit()
        exchange_edit.setObjectName("exchange")
        self.layout().addRow("Exchange", exchange_edit)

        currency_edit = QLineEdit()
        currency_edit.setObjectName("currency")
        self.layout().addRow("Currency", currency_edit)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Save
        )
        self._buttons.accepted.connect(self.on_create)  # type: ignore[union-attr]
        self._buttons.rejected.connect(self.on_reject)  # type: ignore[union-attr]
        self.layout().addWidget(self._buttons)


class TickersTableWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Tickers in Portfolio")

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        book_table = BookTable()

        self.model = QSqlRelationalTableModel(book_table)
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.setTable("tickers")
        book_table.setModel(self.model)

        self.model.setHeaderData(self.model.fieldIndex("symbol"), Qt.Horizontal, "Symbol")
        self.model.setHeaderData(self.model.fieldIndex("exchange"), Qt.Horizontal, "Exchange")
        self.model.setHeaderData(self.model.fieldIndex("currency"), Qt.Horizontal, "Currency")

        book_table.setColumnHidden(self.model.fieldIndex("id"), True)
        book_table.setColumnHidden(self.model.fieldIndex("is_enabled"), True)

        if not self.model.select():
            print(self.model.lastError())

        selection_model = book_table.selectionModel()
        # selection_model.currentRowChanged.connect(mapper.setCurrentModelIndex)

        self.layout().addWidget(book_table)

class MainWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Ticker in Portfolio")

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        tickers_table_widget = TickersTableWidget()
        self.layout().addWidget(tickers_table_widget)

        add_ticker_widget = AddTickerWidget()
        # add_ticker_widget.on_create.connect(self.on_create)
        # add_ticker_widget.on_reject.connect(self.on_reject)
        self.layout().addWidget(add_ticker_widget)

        mapper = QDataWidgetMapper(self)
        mapper.setModel(tickers_table_widget.model)
        mapper.setItemDelegate(TickerDelegate(self))
        # mapper.addMapping(add_ticker_widget.findChild(QLineEdit, "symbol"), tickers_table_widget.model.fieldIndex("symbol"))

        # book_table = BookTable()
        #
        # self.model = QSqlRelationalTableModel(book_table)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        # self.model.setTable("tickers")
        # book_table.setModel(self.model)
        #
        # self.model.setHeaderData(self.model.fieldIndex("symbol"), Qt.Horizontal, "Symbol")
        # self.model.setHeaderData(self.model.fieldIndex("exchange"), Qt.Horizontal, "Exchange")
        # self.model.setHeaderData(self.model.fieldIndex("currency"), Qt.Horizontal, "Currency")
        #
        # book_table.setColumnHidden(self.model.fieldIndex("id"), True)
        # book_table.setColumnHidden(self.model.fieldIndex("is_enabled"), True)
        #
        # if not self.model.select():
        #     print(self.model.lastError())
        #
        # mapper = QDataWidgetMapper(self)
        # mapper.setModel(self.model)
        # mapper.setItemDelegate(TickerDelegate(self))
        # mapper.addMapping(add_ticker_widget.findChild(QLineEdit, "symbol"), self.model.fieldIndex("symbol"))
        #
        # selection_model = book_table.selectionModel()
        # # selection_model.currentRowChanged.connect(mapper.setCurrentModelIndex)
        #
        # self.layout().addWidget(book_table)


    # def on_create(self):
    #     r = self.model.record()
    #     r.setGenerated("id", False)
    #     r.setValue("symbol", self.findChild(QLineEdit, "symbol").text())
    #     r.setValue("exchange", self.findChild(QLineEdit, "exchange").text())
    #     r.setValue("currency", self.findChild(QLineEdit, "currency").text())
    #     r.setValue("is_enabled", True)
    #     result = self.model.insertRecord(-1, r)
    #     print(result)
    #
    # def on_reject(self):
    #     print("reject")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle("FTT")
        self.resize(1000, 600)

        main_widget = MainWidget()
        self.setCentralWidget(main_widget)