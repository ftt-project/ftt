import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_load_securties_step import (
    PortfolioVersionLoadSecuritiesStep,
)


class TestPortfolioVersionLoadSecuritiesStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadSecuritiesStep()

    def test_load_securities(self, subject, portfolio_version, weight):
        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert type(result.value) is list
        assert len(result.value) == 1
        assert result.value[0] == weight.security
