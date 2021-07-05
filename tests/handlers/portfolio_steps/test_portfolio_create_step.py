import pytest

from trade.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from trade.storage.models.portfolio import Portfolio


class TestPortfolioCreateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioCreateStep

    @pytest.fixture
    def data(self):
        return {
            "name": "Example",
            "amount": 10000
        }

    def test_process(self, subject, data):
        result = subject.process(**data)
        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None
