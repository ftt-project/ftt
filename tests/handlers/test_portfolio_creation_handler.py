import pytest

from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.storage.models import Portfolio


class TestPortfolioCreationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioCreationHandler()

    @pytest.fixture
    def arguments(self):
        return {"name": "Portfolio 123"}

    def test_creates_portfolio_with_given_name(self, subject, arguments):
        result = subject.handle(**arguments)

        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None
