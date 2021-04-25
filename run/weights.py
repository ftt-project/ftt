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
from trade.db import Ticker, TickerReturn, DatabaseConnection, Portfolio, Weight


class Weights(BaseCommand):
    """
    Calculates weights of given in configuration tickers
    """

    def calculate(self, persist: bool = False):
        """
        Returns recommended weights of a given portfolio

        TODO: take portfolio id/name as an argument where all weights are 0
        """
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
            portfolio = self.__portfolio()
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
            df = pd.DataFrame({ticker: dataframe.close}, index=dataframe.index)
            dataframes.append(df)
        return pd.concat(dataframes, axis=1).dropna()

    def __ticker_results(self, ticker):
        query = self.__base_query(). \
            where(TickerReturn.ticker == Ticker.get(Ticker.ticker == ticker))
        return query.sql()

    def __persist_weight(self, portfolio, ticker_name, value):
        (Weight.insert(
            portfolio=portfolio,
            ticker=Ticker.get(ticker=ticker_name),
            position=0,
            planned_position=value,
        )
         .on_conflict(
            conflict_target=(Weight.ticker, Weight.portfolio),
            update={Weight.planned_position: value}
        )
         .execute())

    def __base_query(self):
        return TickerReturn.select(
            TickerReturn.datetime,
            TickerReturn.close,
        ).where(
            TickerReturn.interval == '1d',
            TickerReturn.datetime > self.__start_period()
        ).order_by(
            TickerReturn.datetime.asc()
        ).join(Ticker)

    def __portfolio(self):
        return Portfolio.get_by_id(1)

    @staticmethod
    def __start_period():
        return pendulum.naive(2020, 1, 15)

    @staticmethod
    def __tickers():
        return Configuration().scrape().tickers

    @staticmethod
    def __total_portfolio_value():
        return 17000


if __name__ == "__main__":
    try:
        fire.Fire({
            "calculate": Weights().calculate
        })
    except Exception as e:
        chime.error()
        raise e
