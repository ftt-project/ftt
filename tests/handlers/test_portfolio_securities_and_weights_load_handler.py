import pytest

from ftt.handlers.portfolio_handlers import PortfolioSecuritiesAndWeightsLoadHandler
from ftt.storage import schemas


class TestPortfolioWeightsLoadHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioSecuritiesAndWeightsLoadHandler()

    def test_returns_list_of_portfolio_securities_without_portfolio_version(
        self, subject, portfolio, portfolio_security
    ):
        result = subject.handle(
            portfolio=schemas.Portfolio(id=portfolio.id),
            portfolio_version=schemas.PortfolioVersion(),
        )

        assert result.is_ok()
        assert len(result.unwrap()) == 1
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].planned_position is None

    def test_returns_list_of_securities_by_portfolio_with_portfolio_version(
        self, subject, portfolio, portfolio_version, portfolio_security, weight
    ):
        result = subject.handle(
            portfolio=schemas.Portfolio(id=portfolio.id),
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id),
        )

        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].symbol == weight.security.symbol
        assert result.value[0].planned_position == weight.planned_position
