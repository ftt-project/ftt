from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlRelationalTableModel, QSqlTableModel
from PySide6.QtWidgets import QMainWindow, QApplication, QStyleFactory, \
    QGroupBox, QFormLayout, QLineEdit, QVBoxLayout, QDialogButtonBox, QWidget, QHBoxLayout

from ftt.book_table import BookTable


class TickersTableWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Tickers")
        self.setLayout(QVBoxLayout())

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

        search_widget = QWidget(self)
        search_widget.setLayout(QHBoxLayout())
        search_widget.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        search_widget.layout().setContentsMargins(0, 0, 0, 0)
        search_input = QLineEdit()
        search_input.setMaximumWidth(200)
        search_input.setPlaceholderText("Search ticker")
        search_input.setObjectName("search-input")
        search_widget.layout().addWidget(search_input)
        search_button_group = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        search_button_group.setMaximumWidth(100)
        search_button_group.setObjectName("search-button-group")
        search_widget.layout().addWidget(search_button_group)

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