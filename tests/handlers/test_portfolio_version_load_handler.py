import pytest

from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.storage import schemas


class TestPortfolioVersionLoadHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadHandler()

    def test_returns_portfolio_version_by_id(self, subject, portfolio_version):
        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert isinstance(result.value, schemas.PortfolioVersion)
        assert result.value == portfolio_version
