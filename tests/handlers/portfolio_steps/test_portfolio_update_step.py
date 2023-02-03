import pytest

from ftt.handlers.portfolio_steps.portfolio_update_step import PortfolioUpdateStep
from ftt.storage import schemas
from tests.helpers import reload_record


class TestPortfolioUpdateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateStep

    def test_process(self, subject, portfolio):
        portfolio_schema = schemas.Portfolio.from_orm(portfolio)
        portfolio_schema.name = "New portfolio name"
        result = subject.process(portfolio=portfolio_schema)

        assert result.is_ok()
        assert isinstance(result.value, schemas.Portfolio)
        assert reload_record(portfolio).name == "New portfolio name"
