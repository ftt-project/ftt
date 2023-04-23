from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QStyleFactory, \
    QGroupBox, QLineEdit, QVBoxLayout, QDialogButtonBox, QWidget, QHBoxLayout, QCompleter

import yfinance as yf

from ftt import models
from ftt.ticker_table import BookTable
from ftt.workers import TickersLoadWorker


class SearchTickerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = models.tracking_symbols_model_instance()

        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout().setContentsMargins(0, 0, 0, 0)

        search_input = QLineEdit()
        search_input.setMaximumWidth(200)
        search_input.setPlaceholderText("Search ticker")
        search_input.setObjectName("search-input")

        equity_model = models.equity_model_instance()
        completer = QCompleter(self)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCompletionColumn(equity_model.fieldIndex("symbol"))
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setModel(equity_model)
        # completer.activated.connect(search_input.textChanged)
        search_input.setCompleter(completer)
        equity_model.select()

        self.layout().addWidget(search_input)

        search_button_group = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        search_button_group.setMaximumWidth(100)
        search_button_group.setObjectName("search-button-group")
        search_button_group.button(QDialogButtonBox.StandardButton.Ok).setText("Search")
        # search_button_group.clicked.connect(self.on_search_button_clicked)
        self.layout().addWidget(search_button_group)

    def on_search_button_clicked(self, _):
        ticker_value = self.findChild(QLineEdit, "search-input").text()
        ticker = yf.Ticker(ticker_value)

        r = self.model.record()
        r.setGenerated("id", False)
        r.setValue("symbol", ticker.info['symbol'])
        r.setValue("exchange", ticker.info['exchange'])
        r.setValue("currency", ticker.info['currency'])
        r.setValue("is_enabled", True)
        result = self.model.insertRecord(-1, r)
        print(result)


class TickersTableWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Tickers")
        self.setLayout(QVBoxLayout())

        book_table = BookTable()

        self.model = models.tracking_symbols_model_instance()
        self.model.setParent(book_table)

        book_table.setModel(self.model)
        book_table.setColumnHidden(self.model.fieldIndex("id"), True)
        book_table.setColumnHidden(self.model.fieldIndex("is_enabled"), True)

        if not self.model.select():
            print(self.model.lastError())

        search_widget = SearchTickerWidget(self)

        self.layout().addWidget(search_widget)
        self.layout().addWidget(book_table)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        tickers_table_widget = TickersTableWidget()
        self.layout().addWidget(tickers_table_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle("FTT")
        self.resize(1000, 600)

        main_widget = MainWidget()
        self.setCentralWidget(main_widget)

        TickersLoadWorker.perform()
