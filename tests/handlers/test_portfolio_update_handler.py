import pytest

from ftt.handlers.portfolio_update_handler import PortfolioUpdateHandler
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO


class TestPortfolioUpdateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateHandler()

    def test_updates_name(self, subject, portfolio):
        name = "new name"
        result = subject.handle(portfolio=portfolio, dto=PortfolioDTO(name=name))

        assert result.is_ok()
        assert portfolio.name == name
