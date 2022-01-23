from dataclasses import dataclass

import pytest

from ftt.handlers.portfolio_steps.portfolio_delete_step import PortfolioDeleteStep


class TestPortfolioDeleteStep:
    @pytest.fixture
    def subject(self):
        return PortfolioDeleteStep

    def test_process(self, subject, portfolio):
        result = subject.process(portfolio=portfolio)

        assert result.is_ok()
        assert result.value.deleted_at is not None
