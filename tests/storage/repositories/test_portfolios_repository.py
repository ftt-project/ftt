from dataclasses import dataclass

import pytest

from ftt.storage.data_objects.portfolio_dto import PortfolioValueObject
from ftt.storage.errors import PersistingError
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository

from pytest import fixture


class TestPortfoliosRepository:
    @fixture
    def subject(self):
        return PortfoliosRepository

    @fixture
    def data(self):
        return {"name": "Repository 1"}

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name(portfolio.name)
        assert found.id == portfolio.id

    def test_creates_portfolio(self, data, subject):
        result = subject.create(**data)

        assert type(result) == Portfolio
        Portfolio.delete().execute()

    def test_get_securities_for_latest_version(
        self, subject, portfolio, weight, security
    ):
        result = subject.get_securities(portfolio)

        assert type(result) == list
        assert result[0] == security

    def test_save(self, subject, portfolio):
        portfolio.name = "New name"
        result = subject.save(portfolio)

        assert result == portfolio
        assert Portfolio.get(portfolio.id).name == "New name"

    def test_update(self, subject, portfolio):
        dto = PortfolioValueObject(name="New name")
        result = subject.update(portfolio, dto)

        assert result == portfolio
        assert Portfolio.get(portfolio.id).name == "New name"

    def test_update_unknown_fields(self, subject, portfolio):
        @dataclass
        class FakeDTO(PortfolioValueObject):
            field: str = "value"

        dto = FakeDTO(name="New name")
        with pytest.raises(PersistingError) as exc:
            subject.update(portfolio, dto)

        assert "Failed to persist `Portfolio` with params" in str(exc.value)

    def test_update_missing_field(self, subject, portfolio):
        dto = PortfolioValueObject(name="")
        with pytest.raises(PersistingError) as exc:
            subject.update(portfolio=portfolio, dto=dto)

        assert "Failed to persist `Portfolio` with params" in str(exc.value)
        assert "CHECK constraint failed" in str(exc.value)
