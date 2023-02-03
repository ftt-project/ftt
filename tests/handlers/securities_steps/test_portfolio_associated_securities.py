import pytest

from ftt.handlers.securities_steps.portfolio_associated_securities import (
    PortfolioAssociatedSecuritiesStep,
)
from ftt.storage import schemas


class TestPortfolioAssociatedSecuritiesStep:
    @pytest.fixture
    def subject(self):
        return PortfolioAssociatedSecuritiesStep

    def test_process_returns_list_of_securities(
        self, subject, portfolio, security, portfolio_security
    ):
        result = subject.process(portfolio=schemas.Portfolio(id=portfolio.id))

        assert result.is_ok()
        assert result.value[0].id == security.id

    def test_process_returns_error_on_portfolio_missing(self, subject):
        result = subject.process(portfolio=schemas.Portfolio(id=567))

        assert result.is_err()
        assert result.value == "Portfolio with ID 567 is missing"
