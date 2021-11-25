from datetime import datetime

import pytest

from ftt.cli.handlers.create_portfolio_prompts_handler import (
    CreatePortfolioPromptsHandler,
)
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class TestCreatePortfolioPromptsHandler:
    @pytest.fixture
    def subject(self):
        return CreatePortfolioPromptsHandler()

    @pytest.fixture(autouse=True)
    def prompt_mock(self, mocker):
        portfolio_fields_mock = mocker.patch(
            "ftt.cli.handlers.steps.portfolio_fields_prompts_step.prompt"
        )
        portfolio_fields_mock.side_effect = ["Utilities"]

        portfolio_version_mock = mocker.patch(
            "ftt.cli.handlers.steps.portfolio_version_fields_prompts_step.prompt"
        )
        portfolio_version_mock.side_effect = [101.10, "2020-01-01", "2020-06-01", "1d"]

    def test_handle_returns_valid_portfolio_with_all_fields(self, subject):
        result = subject.handle()

        assert result.is_ok()
        assert type(result.value) == dict
        assert type(result.value["portfolio_dto"]) == PortfolioDTO
        assert result.value["portfolio_dto"].name == "Utilities"
        assert type(result.value["portfolio_version_dto"]) == PortfolioVersionDTO
        assert result.value["portfolio_version_dto"].value == 101.10
        assert result.value["portfolio_version_dto"].period_start == datetime(
            2020, 1, 1
        )
        assert result.value["portfolio_version_dto"].period_end == datetime(2020, 6, 1)
        assert result.value["portfolio_version_dto"].interval == "1d"
