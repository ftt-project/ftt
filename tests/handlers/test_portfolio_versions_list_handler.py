import pytest

from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.storage import schemas


class TestPortfolioVersionsListHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsListHandler()

    def test_handle(self, subject, portfolio, portfolio_version):
        result = subject.handle(portfolio=schemas.Portfolio.from_orm(portfolio))

        assert result.is_ok()
        assert result.value[0].id == portfolio_version.id
        assert isinstance(result.value[0], schemas.PortfolioVersion)
