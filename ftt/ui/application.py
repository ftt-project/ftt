from PySide6.QtGui import QGuiApplication
from PySide6.QtQuickControls2 import QQuickStyle

from ftt.application import Environment, APPLICATION_NAME
from ftt.cli.handlers.prepare_environment_handler import PrepareEnvironmentHandler
from ftt.ui.main.models import PortfoliosModel
from ftt.ui.main.views import MainView


class Application(QGuiApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QQuickStyle.setStyle("Material")

        result = PrepareEnvironmentHandler().handle(
            environment=Environment.PRODUCTION, application_name=APPLICATION_NAME
        )

    def run(self):
        # qmlRegisterSingletonType(PortfoliosModel, "PortfoliosModel", 1, 0, "PortfoliosModel", lambda eng: model)

        model = PortfoliosModel()
        model.load()

        window = MainView(model)
        window.show()

        super().exec()
