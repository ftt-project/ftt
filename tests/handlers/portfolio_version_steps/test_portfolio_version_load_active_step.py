import pytest

from trade.handlers.portfolio_version_steps.portfolio_version_load_active_step import PortfolioVersionLoadActiveStep


class TestPortfolioVersionLoadActiveStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadActiveStep

    def test_returns_active_version(self, subject, portfolio, portfolio_version):
        # TODO Move to factory
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio=portfolio)

        assert result.is_ok()
        assert result.value == portfolio_version
