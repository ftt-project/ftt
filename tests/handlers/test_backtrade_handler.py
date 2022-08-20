import pytest

from ftt.handlers.backtrade_handler import BacktradeHandler


class TestBacktradeHandler:
    @pytest.fixture
    def subject(self):
        return BacktradeHandler()

    def test_handle_backtrading_process_and_returns_result(
        self, subject, portfolio_version, security_prices_for_portfolio_version_factory
    ):
        _ = security_prices_for_portfolio_version_factory(portfolio_version)

        result = subject.handle(portfolio_version_id=portfolio_version.id)

        assert result.is_ok()
        assert result.value.original_value == portfolio_version.value
        assert result.value.final_value == 30000.0
