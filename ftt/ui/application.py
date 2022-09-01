from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication


from ftt.application import Environment, APPLICATION_NAME
from ftt.cli.handlers.prepare_environment_handler import PrepareEnvironmentHandler
from ftt.ui.main.views import MainView


class Application(QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        result = PrepareEnvironmentHandler().handle(
            environment=Environment.PRODUCTION, application_name=APPLICATION_NAME
        )

    def run(self):
        window = MainView()
        window.show()

        super().exec()
