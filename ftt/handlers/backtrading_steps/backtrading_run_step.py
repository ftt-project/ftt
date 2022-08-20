from backtrader.feeds import PandasData
from pandas import DataFrame
from result import Result, Ok
import backtrader as bt

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.backtesting_result_dto import BacktestingResultDTO
from ftt.storage.models import PortfolioVersion


class BacktradingRunStep(AbstractStep):
    key = "backtrading_result"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion, security_prices: DataFrame
    ) -> Result[BacktestingResultDTO, str]:
        result = BacktestingResultDTO()
        result.original_value = float(portfolio_version.value)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(float(portfolio_version.value))
        cerebro.addstrategy(bt.Strategy)
        data = PandasData(dataname=security_prices)
        cerebro.adddata(data)
        _ = cerebro.run()
        result.final_value = cerebro.broker.getvalue()

        return Ok(result)
