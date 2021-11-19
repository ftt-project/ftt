import pytest

from ftt.cli.handlers.steps.portfolio_version_fields_prompts_step import (
    PortfolioVersionFieldsPromptsStep, PortfolioVersionDTO,
)


class TestPortfolioVersionFieldsPromptsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionFieldsPromptsStep

    @pytest.fixture(autouse=True)
    def prompt_mock(self, mocker):
        mock = mocker.patch("ftt.cli.handlers.steps.portfolio_version_fields_prompts_step.prompt")
        mock.side_effect = [100, "2010-01-01", "2010-01-01", "1m"]

        return mock

    @pytest.fixture
    def portfolio_version_defaults(self):
        return PortfolioVersionDTO(**{
            "value": 456.10,
            "period_start": "2021-01-01",
            "period_end": "2021-06-01",
            "interval": "1d"
        })

    def test_process_requests_portfolio_version_fields(self, subject, prompt_mock):
        result = subject.process()

        assert result.is_ok()
        prompt_mock.assert_any_call("Account value: ", default=None)
        prompt_mock.assert_any_call("Period start: ", default=None)
        prompt_mock.assert_any_call("Period end: ", default=None)
        prompt_mock.assert_any_call("Interval: ", default=None)

    def test_process_requests_portfolio_version_fields_with_defaults(self, subject, portfolio_version_defaults, prompt_mock):
        result = subject.process(defaults=portfolio_version_defaults)

        assert result.is_ok()
        prompt_mock.assert_any_call("Account value: ", default=portfolio_version_defaults.value)
        prompt_mock.assert_any_call("Period start: ", default=portfolio_version_defaults.period_start)
        prompt_mock.assert_any_call("Period end: ", default=portfolio_version_defaults.period_end)
        prompt_mock.assert_any_call("Interval: ", default=portfolio_version_defaults.interval)
