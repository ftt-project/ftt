import sys

from PySide6.QtWidgets import QApplication

from ftt.application import Environment, APPLICATION_NAME
from ftt.cli.handlers.prepare_environment_handler import PrepareEnvironmentHandler
from ftt.ui.events import PortfolioEventsFilter
from ftt.ui.main_window.models import MainApplicationModel
from ftt.ui.main_window.views import MainWindow


class Application(QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        result = PrepareEnvironmentHandler().handle(
            environment=Environment.PRODUCTION, application_name=APPLICATION_NAME
        )

    def run(self):
        model = MainApplicationModel()
        window = MainWindow(model)
        self.installEventFilter(PortfolioEventsFilter(window))
        window.show()
        sys.exit(super().exec_())
