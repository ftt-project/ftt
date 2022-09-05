from PySide6.QtCore import QObject
from PySide6.QtQuick import QQuickView

from ftt.ui.portfolio.models import PortfolioModel
from ftt.ui.portfolio.views import PortfolioView


class MainView(QQuickView):
    def __init__(self, model):
        super().__init__()
        self.setResizeMode(QQuickView.SizeRootObjectToView)

        self.setInitialProperties({"mainModel": model})
        self.setSource("ftt/ui/main/view.qml")

        model.selectionChanged.connect(self.onSelectionChanged)

        self._portfolio_model = PortfolioModel()
        self.centralWidget = PortfolioView(self._portfolio_model)

        # self.contentRoot.addChild(self.centralWidget)

    def onSelectionChanged(self, portfolio_id):
        print("onSelectionChanged", portfolio_id)
        self._portfolio_model.load(portfolio_id)
        found = self.rootObject().findChild(QObject, "contentRoot")
        self.centralWidget.setParent(found)
