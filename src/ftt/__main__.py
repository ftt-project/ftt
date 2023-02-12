import sys

from PySide6.QtWidgets import QApplication

from ftt import models
from ftt.main_window import MainWindow


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        models.init_db()

        window = MainWindow()
        window.show()

        sys.exit(super().exec())


if __name__ == "__main__":
    app = Application([])

    sys.exit(app.run())
