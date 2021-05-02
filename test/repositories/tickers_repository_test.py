from datetime import datetime

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
            "currency": "USD",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

    @fixture
    def ticker(self, data):
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

    def test_create(self, data, subject):
        result = subject.create(data)

        assert type(result) == Ticker
        assert result.id is not None
        assert result.name == data["name"]
        assert result.exchange == data["exchange"]
        assert result.updated_at is not None
        assert result.created_at is not None
