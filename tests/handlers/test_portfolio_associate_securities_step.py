import pytest

from trade.handlers.portfolio_associate_securities_step import PortfolioAssociateSecuritiesHandler


class TestPortfolioAssociateSecuritiesHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioAssociateSecuritiesHandler()

    def test_associates_portfolio_with_securities(self, subject, portfolio, portfolio_version, security):
        result = subject.handle(
            securities=[security.symbol],
            portfolio_version=portfolio_version
        )

        assert result.is_ok()
        assert result.value == portfolio_version
        assert result.value.weights == [security]
