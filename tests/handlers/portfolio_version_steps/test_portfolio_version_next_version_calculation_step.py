import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_next_version_calculation_step import (
    PortfolioVersionNextVersionCalculationStep,
)


class TestPortfolioVersionNextVersionCalculationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionNextVersionCalculationStep

    def test_process_returns_next_version_number(
        self, subject, portfolio, portfolio_version
    ):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert result.value > portfolio_version.version

    def test_process_returns_next_version_when_no_versions_exist(
        self, subject, portfolio
    ):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert result.value == 1
