from datetime import datetime

import pytest

from ftt.handlers.portfolio_steps.portfolio_version_create_step import (
    PortfolioVersionCreateStep,
)
from ftt.storage import schemas
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolioVersionCreateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionCreateStep

    def test_process_creates_portfolio_version(self, subject, schema_portfolio_version):
        result = subject.process(portfolio_version=schema_portfolio_version, version=1)

        assert result.is_ok()
        assert type(result.value) == schemas.PortfolioVersion
        assert result.value.id is not None
