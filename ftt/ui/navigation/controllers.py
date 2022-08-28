from result import Ok, Err

from ftt.ui.controller import Controller
from ftt.ui.events import PortfolioNavigationEvent


class NavigationController(Controller):
    def initialize_and_render(self):
        self.view.grid(column=0, row=0)
        self.view.grid_propagate(0)

        portfolios_result = self.model.portfolios

        match portfolios_result:
            case Ok(value):
                self.view.add_portfolios(value)
            case Err(error):
                print(error)

    def navigation_clicked(self, portfolio_id):
        self.notify(PortfolioNavigationEvent(portfolio_id=portfolio_id))

    def update(self, event):
        pass
