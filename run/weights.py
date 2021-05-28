from typing import Optional

import fire
import chime
import pendulum
import pandas as pd

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import DiscreteAllocation

from trade.base_command import BaseCommand
from trade.configuration import Configuration
from trade.models import Ticker, TickerReturn, DatabaseConnection, Portfolio, Weight
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.repositories.portfolios_repository import PortfoliosRepository
from trade.repositories.weights_repository import WeightsRepository


class Weights(BaseCommand):
    """
    Calculates weights of given in configuration tickers
    """

    def calculate(self, portfolio_id: int, persist: bool = False) -> None:
        """
        Returns recommended weights of a given portfolio

        TODO: take portfolio id/name as an argument where all weights are 0
        """
        self._portfolio_id = portfolio_id
        dataframes = self.__build_dataframes()

        ticker_returns = dataframes.pct_change().dropna()

        mu = expected_returns.return_model(dataframes, method="capm_return")
        S = risk_models.risk_matrix(dataframes, method="oracle_approximating")

        ef = EfficientFrontier(mu, S)

        raw_weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        ef.portfolio_performance(verbose=True)

        # TODO: take __total_portfolio_value from portfolio itself
        da = DiscreteAllocation(cleaned_weights, dataframes.iloc[-1],
                                total_portfolio_value=self.__total_portfolio_value())
        alloc, leftover = da.lp_portfolio()
        print(f"Leftover: ${leftover:.2f}")
        print(pd.Series(alloc).sort_index())
        if persist:
            portfolio = self.__portfolio(self._portfolio_id)
            for ticker_name, value in alloc.items():
                self.__persist_weight(portfolio, ticker_name, value)

    def __build_dataframes(self):
        dataframes = []
        for ticker in self.__tickers():
            query, params = self.__ticker_results(ticker)
            dataframe = pd.read_sql(query, DatabaseConnection(),
                                    params=params,
                                    index_col='datetime'
                                    )
            df = pd.DataFrame({ticker.symbol: dataframe.close}, index=dataframe.index)
            dataframes.append(df)
        return pd.concat(dataframes, axis=1).dropna()

    def __ticker_results(self, ticker):
        query = self.__base_query(). \
            where(TickerReturn.ticker == Ticker.get(Ticker.symbol == ticker.symbol))
        return query.sql()

    def __base_query(self):
        return TickerReturn.select(
            TickerReturn.datetime,
            TickerReturn.close,
        ).where(
            TickerReturn.interval == '5m',
            TickerReturn.datetime > self.__start_period()
        ).order_by(
            TickerReturn.datetime.asc()
        ).join(Ticker)

    def __persist_weight(self, portfolio, ticker_name, value) -> None:
        WeightsRepository().upsert({
            "portfolio_version": self.__portfolio_version(),
            "ticker": Ticker.get(symbol=ticker_name),
            "position": 0,
            "planned_position": value
        })

    @staticmethod
    def __start_period():
        return pendulum.naive(2021, 5, 20)

    def __tickers(self):
        return PortfoliosRepository.get_tickers(self.__portfolio(self._portfolio_id))

    def __portfolio(self, portfolio_id: int):
        return PortfoliosRepository.get_by_id(portfolio_id)

    def __portfolio_version(self):
        return PortfolioVersionsRepository().get_latest_version(self._portfolio_id)

    @staticmethod
    def __total_portfolio_value():
        return 5000


if __name__ == "__main__":
    try:
        fire.Fire(Weights)
    except Exception as e:
        chime.error()
        raise e
