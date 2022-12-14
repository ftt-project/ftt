from datetime import datetime

import pandas as pd
from pytest import fixture

from ftt.storage import schemas
from ftt.storage.models.security import Security
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class TestSecuritiesRepository:
    @fixture
    def subject(self):
        return SecuritiesRepository

    @fixture
    def data(self):
        return {
            "symbol": "AA.XX",
            "exchange": "SYD",
            "company_name": "Company AAXX",
            "exchange_name": "SYD",
            "quote_type": "Stock",
            "type_display": "Stock",
            "industry": "Technology",
            "sector": "Technology",
            "country": "US",
            "short_name": "Short name",
            "long_name": "Long name",
            "currency": "USD",
        }

    def test_get_by_name(self, security, subject):
        found = subject.get_by_name(security.symbol)

        assert security.id == found.id
        assert type(found) == schemas.Security

    def test_get_by_name_not_found(self, subject):
        result = subject.get_by_name("random-symbol")
        assert result is None

    def test_save(self, security, subject):
        security.symbol = "BB.YY"
        result = subject.save(security)
        found = Security.get_by_id(security.id)

        assert type(result) is Security
        assert found.symbol == "BB.YY"

    def test_upsert_new_record(self, schema_security, subject):
        result, created = subject.upsert(schema_security)

        assert type(result) == Security
        assert result.id is not None
        assert result.symbol == schema_security.symbol
        assert result.exchange == schema_security.exchange
        assert created

    def test_upsert_existing_record(self, data, subject, security):
        result, created = subject.upsert(data)

        assert type(result) == Security
        assert result.id == security.id
        assert not created

    def test_exist(self, subject, security):
        result = subject.exist(security.symbol)
        assert result

        result = subject.exist("random-symbol")
        assert not result

    def test_find_securities(self, subject, portfolio_version, security, weight):
        result = subject.find_securities(portfolio_version)

        assert type(result) == list
        assert result[0] == security

    def test_find_by_portfolio(self, subject, portfolio, portfolio_security):
        result = subject.find_by_portfolio(schemas.Portfolio(id=portfolio.id))

        assert isinstance(result, list)
        assert isinstance(result[0], schemas.Security)
        assert result[0].id == portfolio_security.security.id
