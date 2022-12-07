from datetime import datetime

import pytest

from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.storage import schemas
from ftt.storage import models


class TestPortfolioCreationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioCreationHandler()

    def test_creates_portfolio_with_empty_securities_list(
        self, subject, schema_portfolio
    ):
        result = subject.handle(portfolio=schema_portfolio, securities=[])

        assert result.is_ok()
        assert type(result.value) == models.Portfolio
        assert result.value.id is not None

    def test_creates_portfolio_with_securities_list(
        self, subject, schema_portfolio, security
    ):
        result = subject.handle(
            portfolio=schema_portfolio, securities=[schemas.Security.from_orm(security)]
        )

        assert result.is_ok()
        assert type(result.value) == models.Portfolio
        assert result.value.id is not None
