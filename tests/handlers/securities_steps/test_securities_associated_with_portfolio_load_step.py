import pytest

from ftt.handlers.securities_steps.securities_associated_with_portfolio_load_step import (
    SecuritiesAssociatedWithPortfolioLoadStep,
)
from ftt.storage import schemas


class TestSecuritiesAssociatedWithPortfolioLoadStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesAssociatedWithPortfolioLoadStep

    def test_process_returns_securities_by_portfolio(
        self,
        subject,
        portfolio,
        security,
        portfolio_security,
    ):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.Security)
        assert len(result.value) == 1
        assert result.value[0].symbol == security.symbol

    def test_returns_error_on_no_portfolio(self, subject):
        result = subject.process(schemas.Portfolio(id=567))

        assert result.is_err()
        assert result.value == "Portfolio with id 567 not found"

    def test_returns_error_on_no_securities(self, subject, portfolio):
        result = subject.process(portfolio)

        assert result.is_err()
        assert result.value == f"No securities associated with portfolio {portfolio.id}"
