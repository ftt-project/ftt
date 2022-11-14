from datetime import datetime

import pytest

from ftt.handlers.portfolio_with_version_creation_handler import (
    PortfolioWithVersionCreationHandler,
)
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolioWithVersionCreationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioWithVersionCreationHandler()

    @pytest.fixture
    def arguments(self):
        return {
            "name": "Repository 1",
            "value": 10000,
            "period_start": datetime(2021, 1, 1),
            "period_end": datetime(2021, 4, 25),
            "interval": "1wk",
        }

    def test_creates_portfolio(self, subject, arguments):
        result = subject.handle(**arguments)

        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None

    def test_creates_portfolio_first_version(self, subject, arguments):
        result = subject.handle(**arguments)

        assert result.is_ok()
        assert type(result.value.versions[0]) == PortfolioVersion
        assert result.value.versions[0].id is not None
