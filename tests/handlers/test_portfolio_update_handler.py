import pytest

from ftt.handlers.portfolio_handlers import PortfolioUpdateHandler
from ftt.storage import schemas
from ftt.storage.value_objects import PortfolioValueObject
from tests.helpers import reload_record


class TestPortfolioUpdateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateHandler()

    def test_updates_name(self, subject, portfolio):
        name = "new name"
        portfolio_schema = schemas.Portfolio.from_orm(portfolio)
        portfolio_schema.name = name
        result = subject.handle(portfolio=portfolio_schema)

        assert result.is_ok()
        assert reload_record(portfolio).name == name
