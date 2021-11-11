import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_update_step import (
    PortfolioVersionUpdateStep,
)


class TestPortfolioVersionUpdateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionUpdateStep

    @pytest.fixture
    def params(self):
        return {
            "amount": 1033,
        }

    def test_process_updates_portfolio_version(
        self, subject, portfolio_version, params
    ):
        result = subject.process(portfolio_version=portfolio_version, params=params)

        assert result.is_ok()
        assert portfolio_version.amount == 1033

    def test_process_returns_error_if_unknown_fields(self, subject, portfolio_version):
        wrong_params = {"unknown_field": "value"}
        result = subject.process(
            portfolio_version=portfolio_version, params=wrong_params
        )

        assert result.is_err()
        assert (
            'Unrecognized attribute "unknown_field" for model class <Model: PortfolioVersion>.'
            in result.value
        )

    def test_process_returns_error_if_missing_field(self, subject, portfolio_version):
        result = subject.process(
            portfolio_version=portfolio_version, params={"interval": ""}
        )

        assert result.is_err()
        assert "CHECK constraint failed: length(interval) > 0" in result.value
