from datetime import datetime

import pytest

from ftt.cli.handlers.update_portfolio_prompts_handler import (
    UpdatePortfolioPromptsHandler,
)
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class TestUpdatePortfolioPromptsHandler:
    @pytest.fixture
    def subject(self):
        return UpdatePortfolioPromptsHandler()

    @pytest.fixture(autouse=True)
    def prompt_mock(self, mocker):
        mock = mocker.patch(
            "ftt.cli.handlers.steps.portfolio_version_fields_prompts_step.prompt"
        )
        mock.side_effect = [101.10, "2020-01-01", "2020-06-01", "1d"]

        return mock

    def test_prompts_single_field(self, subject, prompt_mock):
        result = subject.handle(defaults=PortfolioVersionDTO())

        assert result.is_ok()
        assert result.value.value == 101.10
        assert result.value.period_start == datetime(2020, 1, 1)
        assert result.value.period_end == datetime(2020, 6, 1)
        assert result.value.interval == "1d"
