import datetime

import pandas as pd
import pytest


@pytest.fixture
def security_prices_for_portfolio_version_factory(securities_weights_list_factory):
    def _security_prices_factory(
        portfolio_version,
        number_of_securities=5,
        period_start: datetime = datetime.datetime(2020, 1, 1),
        period_end: datetime = datetime.datetime(2020, 12, 31),
        interval: str = "1d",
    ):
        date_range = pd.date_range(start=period_start, end=period_end)

        weights = securities_weights_list_factory(
            portfolio_version,
            n=number_of_securities,
            interval=interval,
            date_range=date_range,
        )
        return [weight.security for weight in weights]

    yield _security_prices_factory


@pytest.fixture
def security_prices_dataframe_factory(
    securities_weights_list_factory, security_prices_for_portfolio_version_factory
):
    def _security_prices_dataframe_factory(
        portfolio_version,
        number_of_securities=5,
        period_start: datetime = datetime.datetime(2020, 1, 1),
        period_end: datetime = datetime.datetime(2020, 12, 31),
        interval: str = "1d",
    ):
        securities = security_prices_for_portfolio_version_factory(
            portfolio_version, number_of_securities, period_start, period_end, interval
        )

        from ftt.handlers.security_prices_steps.security_prices_dataframe_load_step import (
            SecurityPricesDataframeLoadStep,
        )

        dataframe = SecurityPricesDataframeLoadStep.process(
            portfolio_version_securities=securities,
            portfolio_version=portfolio_version,
        ).value

        return dataframe

    yield _security_prices_dataframe_factory
