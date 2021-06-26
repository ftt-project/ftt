from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.storage.models import Security
from trade.storage.repositories import SecuritiesRepository


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
            "type": "Stock",
            "type_display": "Stock",
            "industry": "Technologie",
            "currency": "USD"
        }

    @fixture
    def ticker(self, data):
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        ticker = Security.create(**data)
        yield ticker
        ticker.delete_instance()
        return ticker

    def test_get_by_name(self, ticker, subject):
        found = subject.get_by_name(ticker.symbol)
        assert ticker.id == found.id

    def test_save(self, ticker, subject):
        ticker.symbol = "BB.YY"
        result = subject.save(ticker)
        found = Security.get_by_id(ticker.id)

        assert type(result) is Security
        assert found.symbol == "BB.YY"

    def test_upsert_new_record(self, data, subject):
        result, created = subject.upsert(pd.Series(data))

        assert type(result) == Security
        assert result.id is not None
        assert result.symbol == data["symbol"]
        assert result.exchange == data["exchange"]
        assert result.updated_at is not None
        assert result.created_at is not None
        assert created

    def test_upsert_existing_record(self, data, subject, ticker):
        result, created = subject.upsert(pd.Series(data))

        assert type(result) == Security
        assert result.id == ticker.id
        assert not created

    def test_exist(self, subject, ticker):
        result = subject.exist(ticker.symbol)
        assert result

        result = subject.exist('random-symbol')
        assert not result
