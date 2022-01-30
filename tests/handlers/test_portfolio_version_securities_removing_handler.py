import pytest

from ftt.handlers.portfolio_version_securities_disassociate_handler import (
    PortfolioVersionSecuritiesDisassociateHandler,
)


class TestPortfolioVersionSecuritiesDisassociateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionSecuritiesDisassociateHandler()

    def test_handle_disassociates_securities_from_portfolio_version(
        self, subject, security, weight, portfolio_version
    ):
        result = subject.handle(
            portfolio_version_id=portfolio_version.id, securities=[security]
        )

        assert result.is_ok()
        assert portfolio_version.weights.count() == 0

    def test_handle_returns_error_if_portfolio_version_not_found(
        self, subject, security, weight, portfolio_version
    ):
        result = subject.handle(portfolio_version_id=19, securities=[security])

        assert result.is_err()
        assert result.unwrap_err() == "Portfolio Version with ID 19 does not exist"

    def test_handle_returns_error_if_weights_are_not_associated(
        self, subject, security, portfolio_version
    ):
        result = subject.handle(
            portfolio_version_id=portfolio_version.id, securities=[security]
        )

        assert result.is_err()

        assert (
            result.unwrap_err()
            == f"Weight AA.XX associated with portfolio version #{portfolio_version.id} not found"
        )
