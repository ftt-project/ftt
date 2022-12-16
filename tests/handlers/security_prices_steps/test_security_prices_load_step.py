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
        weight_factory,
        security_price_factory,
    ):
        security = security_factory()
        weight_factory(portfolio_version, security)
        security_price = security_price_factory(
            security,
            dt=portfolio.period_start,
            interval=portfolio.interval,
        )

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version),
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        assert result.is_ok()
        assert result.value.prices == {security.symbol: [security_price.close]}

    def test_process_returns_error_on_data_points_num_mismatch(
        self,
        subject,
        portfolio_version,
        portfolio,
        security_factory,
        weight_factory,
        security_price_factory,
    ):
        security1 = security_factory(symbol="AA")
        security2 = security_factory(symbol="BB")
        weight_factory(portfolio_version, security1)
        weight_factory(portfolio_version, security2)
        _ = security_price_factory(
            security1,  # only for security 1
            dt=portfolio.period_start,
            interval=portfolio.interval,
        )

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version),
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        assert result.is_err()
        assert (
            result.unwrap_err() == "Data points shapes do not match: {'AA': 1, 'BB': 0}"
        )
