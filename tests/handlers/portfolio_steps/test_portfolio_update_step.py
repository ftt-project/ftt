import pytest

from ftt.handlers.portfolio_steps.portfolio_update_step import PortfolioUpdateStep


class TestPortfolioUpdateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateStep

    @pytest.fixture
    def params(self):
        return {
            'name': 'New Portfolio Name',
        }

    @pytest.fixture
    def wrong_params(self):
        return {
            'wrong_field': 'wrong value'
        }

    def test_process(self, subject, portfolio, params):
        result = subject.process(portfolio=portfolio, params=params)

        assert result.is_ok()
        assert result.value.name == params['name']

    def test_process_unknown_fields(self, subject, portfolio, wrong_params):
        result = subject.process(portfolio=portfolio, params=wrong_params)

        assert result.is_err()
        assert 'Unrecognized attribute "wrong_field" for model class <Model: Portfolio>.' in result.value

    def test_process_missing_field(self, subject, portfolio):
        result = subject.process(portfolio=portfolio, params={"name": ""})

        assert result.is_err()
        assert 'CHECK constraint failed: length(name) > 0' in result.value
