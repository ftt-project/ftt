import datetime

import pytest

from ftt.storage import schemas
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

    def test_security_price_time_vector(self, subject, security, security_price):
        result = subject.security_price_time_vector(
            security=schemas.Security.from_orm(security),
            interval=security_price.interval,
            period_start=(security_price.datetime - datetime.timedelta(days=1)),
            period_end=(security_price.datetime + datetime.timedelta(days=1)),
        )

        assert len(result) == 1
        assert isinstance(result[0], schemas.SecurityPrice)
        assert result[0].symbol == security.symbol
