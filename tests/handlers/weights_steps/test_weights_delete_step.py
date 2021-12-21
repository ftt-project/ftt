import pytest

from ftt.handlers.weights_steps.weights_delete_step import WeightsDeleteStep


class TestWeightsDeleteStep:
    @pytest.fixture
    def subject(self):
        return WeightsDeleteStep

    def test_process_deletes_weights_by_portfolio_version_and_weights(
        self, subject, security, weight, portfolio_version
    ):
        result = subject.process(
            securities=[security], portfolio_version=portfolio_version
        )

        assert result.is_ok()
        assert portfolio_version.weights.count() == 0

    def test_process_returns_error_on_no_weights(
        self, subject, security, portfolio_version
    ):
        result = subject.process(
            securities=[security], portfolio_version=portfolio_version
        )

        assert result.is_err()
        assert (
            result.err()
            == "Weight AA.XX associated with portfolio version #1 not found"
        )
