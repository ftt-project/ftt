from unittest.mock import ANY

import pytest

from ftt.cli.handlers.steps.portfolio_version_fields_prompts_step import (
    PortfolioVersionFieldsPromptsStep,
    PortfolioVersionDTO,
)


class TestPortfolioVersionFieldsPromptsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionFieldsPromptsStep

    @pytest.fixture(autouse=True)
    def prompt_mock(self, mocker):
        mock = mocker.patch(
            "ftt.cli.handlers.steps.portfolio_version_fields_prompts_step.prompt"
        )
        mock.side_effect = [100, "2010-01-01", "2010-01-01", "1m"]

        return mock

    @pytest.fixture
    def portfolio_version_defaults(self):
        return PortfolioVersionDTO(
            **{
                "value": 456.10,
                "period_start": "2021-01-01",
                "period_end": "2021-06-01",
                "interval": "1d",
            }
        )

    def test_process_requests_portfolio_version_fields(self, subject, prompt_mock):
        result = subject.process()

        assert result.is_ok()
        prompt_mock.assert_any_call(
            "Account value: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Period start: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Period end: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Interval: ", default=ANY, placeholder=ANY, validator=ANY
        )

    def test_process_requests_portfolio_version_fields_with_defaults(
        self, subject, portfolio_version_defaults, prompt_mock
    ):
        result = subject.process(defaults=portfolio_version_defaults)

        assert result.is_ok()

        prompt_mock.assert_any_call(
            "Account value: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Period start: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Period end: ", default=ANY, placeholder=ANY, validator=ANY
        )
        prompt_mock.assert_any_call(
            "Interval: ", default=ANY, placeholder=ANY, validator=ANY
        )
