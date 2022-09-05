from PySide6.QtQuick import QQuickView
from PySide6.QtQuickWidgets import QQuickWidget


class PortfolioView(QQuickWidget):
    def __init__(self, model):
        super().__init__()

        self.setInitialProperties({"portfolioVersions": model})

        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setSource("ftt/ui/portfolio/view.qml")

