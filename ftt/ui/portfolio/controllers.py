from tkinter import NW

from result import Err, Ok

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.ui.controller import Controller
from ftt.ui.events import PortfolioNavigationEvent, PortfolioSingleVersionSelectedEvent, \
    PortfolioMultipleVersionsSelectedEvent
from ftt.ui.portfolio.views import PortfolioVersionWeightsView, PortfolioVersionsView, PortfolioPlotView


class PortfolioController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

        self._portfolio_version_weights_controller = PortfolioVersionWeightsController(
            None,
            PortfolioVersionWeightsView(self.view)
        )
        self._portfolio_versions_controller = PortfolioVersionsController(None, PortfolioVersionsView(self.view))
        self._portfolio_plot_controller = PortfolioPlotController(None, PortfolioPlotView(self.view))

        for observer in self._observers:
            self._portfolio_version_weights_controller.attach(observer)
            self._portfolio_versions_controller.attach(observer)
            self._portfolio_plot_controller.attach(observer)

    def initialize_and_render(self):
        self.view.grid(column=1, row=0, sticky=NW)

        self._portfolio_versions_controller.initialize_and_render()
        self._portfolio_version_weights_controller.initialize_and_render()
        self._portfolio_plot_controller.initialize_and_render()

    def update(self, event):
        match event:
            case PortfolioNavigationEvent(portfolio_id=portfolio_id):
                self.handle_portfolio_switch_event(portfolio_id)

    def handle_portfolio_switch_event(self, portfolio_id):
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        match portfolio_result:
            case Ok(value):
                self.view.show_portfolio(value)
            case Err(error):
                print(error)

        versions_result = PortfolioVersionsListHandler().handle(
            portfolio=portfolio_result.value
        )
        if versions_result.is_ok() and versions_result.value is not None:
            match versions_result:
                case Ok(value):
                    self._portfolio_versions_controller.versions = value
                case Err(error):
                    print(error)
        else:
            self._portfolio_versions_controller.versions = []


class PortfolioVersionsController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

        self._versions = None

    def initialize_and_render(self):
        self.view.grid(column=0, row=1, sticky=NW)

    def update(self, event):
        pass

    @property
    def versions(self):
        return self._versions

    @versions.setter
    def versions(self, versions):
        self._versions = versions
        self.view.remove_all_rows()
        for version in versions:
            self.view.add_row(version)

    def on_select_version(self, items):
        match len(items):
            case 0:
                return
            case 1:
                version_id = int(items[0])
                self.notify(PortfolioSingleVersionSelectedEvent(version_id=version_id))
            case _:
                self.notify(PortfolioMultipleVersionsSelectedEvent(version_ids=items))


class PortfolioVersionWeightsController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)
        self._weights = None

    def initialize_and_render(self):
        self.view.grid(column=0, row=2, sticky=NW)

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights):
        self._weights = weights
        self.view.remove_all_rows()
        for weight in weights:
            self.view.add_row(weight)

    def update(self, event):
        match event:
            case PortfolioNavigationEvent(portfolio_id=_):
                self.weights = []
            case PortfolioSingleVersionSelectedEvent(version_id=version_id):
                self.handle_version_selected(version_id)

    def handle_version_selected(self, version_id):
        result_version = PortfolioVersionLoadHandler().handle(portfolio_version_id=version_id)
        if result_version.is_ok():
            weights_result = WeightsListHandler().handle(
                portfolio_version=result_version.value
            )
            match weights_result:
                case Ok(value):
                    self.weights = value
                case Err(error):
                    print(error)
        else:
            print(result_version.error)


class PortfolioPlotController(Controller):
    def initialize_and_render(self):
        self.view.grid(column=0, row=3, sticky=NW)

    def update(self, event):
        match event:
            case PortfolioSingleVersionSelectedEvent(version_id=version_id):
                self.handle_version_selected(version_id)

    def handle_version_selected(self, version_id):
        from ftt.handlers.security_prices_steps.security_prices_load_step import SecurityPricesLoadStep
        from pandas import DataFrame
        import pandas as pd
        import bt

        portfolio_version_result = PortfolioVersionLoadHandler().handle(portfolio_version_id=version_id)

        prices_result = SecurityPricesLoadStep.process(portfolio_version=portfolio_version_result.value)
        data = prices_result.value.prices
        data["Date"] = prices_result.value.datetime_list
        dataframe = DataFrame.from_dict(prices_result.value.prices)
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])  # only in case of daily interval
        dataframe.set_index("Date", inplace=True)
        # print(dataframe)
        # print(dataframe.index.dtype)
        s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
        test = bt.Backtest(s, dataframe)
        res = bt.run(test)
        k = res.plot()
        self.view.plot(k)
        res.display()
