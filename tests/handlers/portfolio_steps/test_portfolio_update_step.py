from dataclasses import dataclass

import pytest

from ftt.handlers.portfolio_steps.portfolio_update_step import PortfolioUpdateStep
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO


class TestPortfolioUpdateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateStep

    @pytest.fixture
    def portfolio_dto(self):
        return PortfolioDTO(
            name="New portfolio name",
        )

    def test_process(self, subject, portfolio, portfolio_dto):
        result = subject.process(portfolio=portfolio, dto=portfolio_dto)

        assert result.is_ok()
        assert result.value.name == portfolio_dto.name

    def test_process_returns_error_if_unknown_fields(self, subject, portfolio):
        @dataclass
        class FakeDTO(PortfolioDTO):
            wrong_field: str

        fake_dto = FakeDTO(wrong_field="value", name="Name")
        result = subject.process(portfolio=portfolio, dto=fake_dto)

        assert result.is_err()
        assert (
            'Unrecognized attribute "wrong_field" for model class <Model: Portfolio>.'
            in result.value
        )

    def test_process_returns_error_if_missing_field(self, subject, portfolio):
        result = subject.process(portfolio=portfolio, dto=PortfolioDTO(name=""))

        assert result.is_err()
        assert "CHECK constraint failed: length(name) > 0" in result.value
