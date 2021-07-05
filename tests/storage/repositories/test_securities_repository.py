from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.storage.models.security import Security
from trade.storage.repositories.securities_repository import SecuritiesRepository


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
            "currency": "USD"
        }

    # @fixture
    # def security(self, data):
    #     data["updated_at"] = datetime.now()
    #     data["created_at"] = datetime.now()
    #     security = Security.create(**data)
    #     yield security
    #     security.delete_instance()
    #     return security

    def test_get_by_name(self, security, subject):
        found = subject.get_by_name(security.symbol)
        assert security.id == found.id

    def test_save(self, security, subject):
        security.symbol = "BB.YY"
        result = subject.save(security)
        found = Security.get_by_id(security.id)

        assert type(result) is Security
        assert found.symbol == "BB.YY"

    def test_upsert_new_record(self, data, subject):
        result, created = subject.upsert(data)

        assert type(result) == Security
        assert result.id is not None
        assert result.symbol == data["symbol"]
        assert result.exchange == data["exchange"]
        assert result.updated_at is not None
        assert result.created_at is not None
        assert created

    def test_upsert_existing_record(self, data, subject, security):
        result, created = subject.upsert(data)

        assert type(result) == Security
        assert result.id == security.id
        assert not created

    def test_exist(self, subject, security):
        result = subject.exist(security.symbol)
        assert result

        result = subject.exist('random-symbol')
        assert not result

    def test_find_securities(self, subject, portfolio_version, security, weight):
        result = subject.find_securities(portfolio_version)

        assert type(result) == list
        assert result[0] == security
