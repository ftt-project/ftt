import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_allocation_step import (
    PortfolioVersionAllocationStep,
)


class TestPortfolioVersionAllocationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionAllocationStep

    @pytest.mark.skip(reason="Not implemented yet")
    def test_run(self, subject):
        pass
