import pytest

from ftt.handlers.security_prices_steps.security_prices_load_step import (
    SecurityPricesLoadStep,
)


class TestSecurityPricesLoadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesLoadStep

    def test_process_returns_security_prices_by_portfolio_version(
        self,
        subject,
        portfolio_version,
        security_factory,
        weight_factory,
        security_price_factory,
    ):
        security = security_factory()
        weight_factory(portfolio_version, security)
        security_price = security_price_factory(
            security,
            dt=portfolio_version.period_start,
            interval=portfolio_version.interval,
        )

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert result.value.prices == {security.symbol: [security_price.close]}