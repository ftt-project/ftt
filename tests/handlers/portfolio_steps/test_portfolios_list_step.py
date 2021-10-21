import pytest

from ftt.handlers.portfolio_steps.portfolios_list_step import PortfoliosListStep


class TestPortfoliosListStep:
    @pytest.fixture
    def subject(self):
        return PortfoliosListStep

    def test_returns_list_of_available_repositories(self, subject, portfolio):
        result = subject.process()

        assert result.is_ok()
        assert result.value[0] == portfolio
