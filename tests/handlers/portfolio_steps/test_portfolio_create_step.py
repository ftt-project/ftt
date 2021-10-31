import pytest

from ftt.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from ftt.storage.models.portfolio import Portfolio


class TestPortfolioCreateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioCreateStep

    @pytest.fixture
    def arguments(self):
        return {
            "name": "Example",
        }

    def test_process(self, subject, arguments):
        result = subject.process(**arguments)
        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None
