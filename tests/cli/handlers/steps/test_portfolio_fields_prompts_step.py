from unittest.mock import ANY

import pytest

from ftt.cli.handlers.steps.portfolio_fields_prompts_step import (
    PortfolioFieldsPromptsStep,
)
from ftt.storage.value_objects import PortfolioValueObject


class TestPortfolioFieldsPromptsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioFieldsPromptsStep

    @pytest.fixture
    def prompt_mock(self, mocker):
        mock = mocker.patch(
            "ftt.cli.handlers.steps.portfolio_fields_prompts_step.prompt"
        )
        mock.side_effect = ["Utilities"]

        return mock

    def test_process_requests_portfolio_fields(self, subject, prompt_mock):
        result = subject.process()

        assert result.is_ok()
        prompt_mock.assert_any_call("Portfolio name: ", placeholder=ANY, validator=ANY)

    def test_process_returns_dto(self, subject, prompt_mock):
        result = subject.process()

        assert type(result.value) == PortfolioValueObject
        assert result.value.name == "Utilities"
