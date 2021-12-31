import datetime

import pytest

from ftt.storage.models.security_price import SecurityPrice
from ftt.storage.repositories.security_prices_repository import SecurityPricesRepository


class TestSecurityPricesRepository:
    @pytest.fixture
    def subject(self):
        return SecurityPricesRepository

    @pytest.fixture
    def data(self, security):
        return {
            "security": security,
            "datetime": datetime.datetime.today(),
            "open": 100,
            "high": 101,
            "low": 99,
            "close": 101,
            "volume": 9999999,
            "interval": "1d",
            "change": 0,
            "percent_change": 1,
        }

    def test_upsert_new_record(self, subject, data, security):
        result, flag = subject.upsert(data)
        assert flag
        assert type(result) == SecurityPrice
        assert result.security == security
        assert result.id is not None

    def test_upsert_existing_record(self, subject, data):
        result1, flag = subject.upsert(data)
        assert flag
        result2, flag = subject.upsert(data)
        assert flag is not True
        assert result1 == result2

    def test_find_by_security_prices_returns_list_of_prices(
        self, subject, security, security_price
    ):
        result = subject.find_by_security_prices(
            security=security,
            interval=security_price.interval,
            period_start=(security_price.datetime - datetime.timedelta(days=1)),
            period_end=(security_price.datetime + datetime.timedelta(days=1)),
        )

        assert len(result) == 1
        assert result[0] == security_price
