from PyQt6.QtWidgets import QTableView


class CentralFrameView(QTableView):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)
        self.parent = parent
        self.model = model

        self.init_ui()

    def init_ui(self):
        pass