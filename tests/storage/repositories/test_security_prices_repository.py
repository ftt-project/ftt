from datetime import datetime

import pytest

from trade.storage.models.security_price import SecurityPrice
from trade.storage.repositories.security_prices_repository import (
    SecurityPricesRepository,
)


class TestSecurityPricesRepository:
    @pytest.fixture
    def subject(self):
        return SecurityPricesRepository

    @pytest.fixture
    def data(self, security):
        return {
            "security": security,
            "datetime": datetime.today(),
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
