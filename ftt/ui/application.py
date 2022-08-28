import tkinter as tk
from tkinter import ttk

from ftt.application import Environment, APPLICATION_NAME
from ftt.cli.handlers.prepare_environment_handler import PrepareEnvironmentHandler
from ftt.ui.main.controllers import MainController
from ftt.ui.main.views import MainView
from ftt.ui.navigation.models import PortfoliosModel
from ftt.ui.portfolio.controllers import PortfolioController
from ftt.ui.navigation.controllers import NavigationController
from ftt.ui.observers.navigation_observer import NavigationObserver
from ftt.ui.observer_registry import ObserverRegistry
from ftt.ui.navigation.views import NavigationView
from ftt.ui.portfolio.views import PortfolioView


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        result = PrepareEnvironmentHandler().handle(
            environment=Environment.PRODUCTION, application_name=APPLICATION_NAME
        )

        self.title("Financial Trading Tools")
        self.geometry("1100x600")
        self.resizable(True, True)

        ObserverRegistry.register(NavigationObserver())

        root = MainView(self)
        self.main_controller = MainController(None, root)
        self.main_controller.initialize_and_render()

        self.navigation_controller = NavigationController(PortfoliosModel(), NavigationView(root))
        self.navigation_controller.attach(ObserverRegistry.get_observer("NavigationObserver"))
        self.navigation_controller.initialize_and_render()

        self.portfolio_controller = PortfolioController(None, PortfolioView(root))
        self.portfolio_controller.attach(ObserverRegistry.get_observer("NavigationObserver"))
        self.portfolio_controller.initialize_and_render()

    def run(self) -> None:
        self.mainloop()
