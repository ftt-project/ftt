from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.models import Ticker
from trade.repositories import TickersRepository


class TestTickersRepository:
    @fixture
    def subject(self):
        return TickersRepository()

    @fixture
    def data(self):
        return {
            "name": "AA.XX",
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
        ticker = Ticker.create(**data)
        yield ticker
        ticker.delete_instance()
        return ticker

    @fixture(autouse=True)
    def cleanup(self):
        yield
        Ticker.delete().execute()

    def test_get_by_name(self, ticker, subject):
        found = subject.get_by_name(ticker.name)
        assert ticker.id == found.id

    def test_save(self, ticker, subject):
        ticker.name = "BB.YY"
        result = subject.save(ticker)
        found = Ticker.get_by_id(ticker.id)

        assert type(result) is Ticker
        assert found.name == "BB.YY"

    def test_upsert_new_record(self, data, subject):
        result, created = subject.upsert(pd.Series(data))

        assert type(result) == Ticker
        assert result.id is not None
        assert result.name == data["name"]
        assert result.exchange == data["exchange"]
        assert result.updated_at is not None
        assert result.created_at is not None
        assert created

    def test_upsert_existing_record(self, data, subject, ticker):
        result, created = subject.upsert(pd.Series(data))

        assert type(result) == Ticker
        assert result.id == ticker.id
        assert not created

    def test_exist(self, subject, ticker):
        result = subject.exist(ticker.name)
        assert result

        result = subject.exist('random-name')
        assert not result
