import backtrader as bt

from trade.storage.repositories.orders_repository import OrdersRepository
from trade.storage.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.storage.repositories.securities_repository import SecuritiesRepository
from trade.storage.repositories.weights_repository import WeightsRepository


class PeakObserver(bt.Observer):
    lines = ("peak",)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(peak=dict(markersize=1.0, color="lime", fillstyle="full"),)

    def next(self):
        portfolio_version_id = self._owner.p.portfolio_version_id
        portfolio = PortfolioVersionsRepository.get_portfolio(portfolio_version_id)
        for data in self.datas:
            name = data._name
            close = data.close[0]
            security = SecuritiesRepository.get_by_name(name)
            order = OrdersRepository.last_successful_order(
                security=security, portfolio=portfolio, type="buy"
            )
            weight = WeightsRepository.find_by_security_and_portfolio(
                security=security, portfolio_version_id=portfolio_version_id
            )
            execution_price = order.execution_price if order else 0
            max_value = max(weight.peaked_value, close, execution_price)
            self.lines.peak[0] = max_value
            WeightsRepository.update_peaked_value(weight, max_value)
