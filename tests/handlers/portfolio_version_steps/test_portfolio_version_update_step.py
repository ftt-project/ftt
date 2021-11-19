from dataclasses import dataclass

import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_update_step import (
    PortfolioVersionUpdateStep,
)
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class TestPortfolioVersionUpdateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionUpdateStep

    @pytest.fixture
    def portfolio_version_dto(self):
        return PortfolioVersionDTO(value=1033)

    def test_process_updates_portfolio_version(
        self, subject, portfolio_version, portfolio_version_dto
    ):
        result = subject.process(
            portfolio_version=portfolio_version, dto=portfolio_version_dto
        )

        assert result.is_ok()
        assert portfolio_version.value == portfolio_version_dto.value

    def test_process_returns_error_if_unknown_fields(self, subject, portfolio_version):
        @dataclass
        class UnknownDTO(PortfolioVersionDTO):
            unknown_field: int = 9

        dto = UnknownDTO(unknown_field="value")
        result = subject.process(portfolio_version=portfolio_version, dto=dto)

        assert result.is_err()
        assert (
            'Unrecognized attribute "unknown_field" for model class <Model: PortfolioVersion>.'
            in result.value
        )

    def test_process_returns_error_if_missing_field(self, subject, portfolio_version):
        result = subject.process(
            portfolio_version=portfolio_version,
            dto=PortfolioVersionDTO(interval="", value=1),
        )

        assert result.is_err()
        assert "CHECK constraint failed: length(interval) > 0" in result.value
