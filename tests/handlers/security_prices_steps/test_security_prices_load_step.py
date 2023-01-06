import pytest

from ftt.handlers.security_prices_steps.security_prices_load_step import (
    SecurityPricesLoadStep,
)
from ftt.storage import schemas


class TestSecurityPricesLoadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesLoadStep

    def test_process_returns_security_prices_by_portfolio_version(
        self,
        subject,
        portfolio_version,
        portfolio,
        security_factory,
        security_price_factory,
        portfolio_security_factory,
    ):
        security = security_factory()
        security_price = security_price_factory(
            security,
            dt=portfolio.period_start,
            interval=portfolio.interval,
        )
        portfolio_security_factory(portfolio, security)

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version),
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        assert result.is_ok()
        assert isinstance(result.value, list)
        assert result.value[0].security.symbol == security.symbol
        assert result.value[0].prices == [security_price.close]
        assert result.value[0].time_vector == [security_price.datetime]

    def test_process_returns_error_on_data_points_num_mismatch(
        self,
        subject,
        portfolio_version,
        portfolio,
        security_factory,
        security_price_factory,
        portfolio_security_factory,
    ):
        security1 = security_factory(symbol="AA")
        portfolio_security_factory(portfolio, security1)
        _ = security_price_factory(
            security1,  # only for security 1
            dt=portfolio.period_start,
            interval=portfolio.interval,
        )

        security2 = security_factory(symbol="BB")
        portfolio_security_factory(portfolio, security2)

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version),
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        assert result.is_err()
        assert (
            result.unwrap_err() == "Data points shapes do not match: {'AA': 1, 'BB': 0}"
        )
