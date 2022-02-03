import pytest

from ftt.handlers.portfolio_version_load_active_handler import (
    PortfolioVersionLoadActiveHandler,
)


class TestPortfolioVersionLoadActiveHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadActiveHandler()

    def test_process_returns_active_portfolio_version_by_portfolio_id(
        self, subject, portfolio_version_factory, portfolio
    ):
        active_portfolio_version = portfolio_version_factory(
            portfolio=portfolio, version=1
        )
        active_portfolio_version.active = True
        active_portfolio_version.save()
        _ = portfolio_version_factory(portfolio=portfolio, version=2)

        result = subject.handle(portfolio_id=portfolio.id)

        assert result.is_ok()
        assert result.value == active_portfolio_version
