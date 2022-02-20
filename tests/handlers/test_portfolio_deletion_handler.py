import pytest

from ftt.handlers.portfolio_deletion_handler import PortfolioDeletionHandler
from tests.helpers import reload_record


class TestPortfolioDeletionHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioDeletionHandler()

    def test_deletion_portfolio_by_id(self, subject, portfolio):
        result = subject.handle(portfolio_id=portfolio.id)

        assert result.is_ok()
        assert result.value == portfolio
        assert reload_record(portfolio).deleted_at is not None

    def test_handle_portfolio_with_active_portfolio_version(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.handle(portfolio_id=portfolio.id)

        assert result.is_err()

    def test_handle_portfolio_with_not_active_portfolio_version(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(portfolio_id=portfolio.id)

        assert result.is_ok()
