import pandas as pd
import pytest

from ftt.handlers.security_prices_steps.security_prices_upsert_step import (
    SecurityPricesUpsertStep,
)
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionValueObject


class TestSecurityPricesUpsertStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesUpsertStep

    @pytest.fixture
    def data(self, security):
        return {
            security.symbol: pd.DataFrame(
                data={
                    "Adj Close": [124.279999, 125.059998, 123.540001],
                    "Close": [124.279999, 125.059998, 123.540001],
                    "High": [125.349998, 125.239998, 124.849998],
                    "Low": [123.940002, 124.050003, 123.129997],
                    "Open": [125.080002, 124.279999, 124.680000],
                    "Volume": [67637100, 59278900, 76229200],
                },
                index=pd.DatetimeIndex(
                    [
                        "2021-06-01 01:01:01",
                        "2021-06-02 01:01:01",
                        "2021-06-03 01:01:01",
                    ]
                ),
            ).rename_axis("Date")
        }

    @pytest.fixture
    def portfolio_version_dto(self):
        return PortfolioVersionValueObject(interval="5m")

    def test_persists_historical_prices(
        self, subject, data, security, security_price, portfolio_version_dto
    ):
        result = subject.process(data, portfolio_version_dto)

        assert result.is_ok()
        assert type(result.value) == dict
        assert result.value[security.symbol] == 3

    def test_upserts_historical_prices(
        self, subject, data, security, security_price, portfolio_version_dto
    ):
        subject.process(data, portfolio_version_dto)
        result = subject.process(data, portfolio_version_dto)
        assert result.value[security.symbol] == 0
