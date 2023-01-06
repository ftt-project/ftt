from dataclasses import dataclass

import pytest

from ftt.storage import schemas
from ftt.storage.value_objects import PortfolioValueObject
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

    def test_get_by_id(self, subject, portfolio):
        result = subject.get_by_id(schemas.Portfolio.from_orm(portfolio))

        assert result.id == portfolio.id

    def test_get_by_id_returns_none(self, subject, portfolio):
        result = subject.get_by_id(schemas.Portfolio(id=999))

        assert result is None

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name(portfolio.name)
        assert found.id == portfolio.id

    def test_create(self, schema_portfolio, subject):
        assert schema_portfolio.id is None

        result = subject.create(schema_portfolio)

        assert type(result) == Portfolio
        assert result.id is not None

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

    def test_find_by_portfolio_version(self, subject, portfolio_version):
        result = subject.find_by_portfolio_version(
            schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert isinstance(result, schemas.Portfolio)
        assert result.id == portfolio_version.portfolio_id
