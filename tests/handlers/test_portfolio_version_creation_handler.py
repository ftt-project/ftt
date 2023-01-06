import pytest

from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.storage import schemas
from ftt.storage.models import PortfolioVersion


class TestPortfolioVersionCreateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionCreationHandler()

    def test_creates_new_version(self, subject, portfolio, schema_portfolio_version):
        schema_portfolio_version.portfolio = schemas.Portfolio(id=portfolio.id)
        result = subject.handle(
            portfolio_version=schema_portfolio_version,
        )

        assert result.is_ok()
        assert type(result.value) == schemas.PortfolioVersion
        assert result.value.portfolio.id == portfolio.id
        assert result.value.version == 1
