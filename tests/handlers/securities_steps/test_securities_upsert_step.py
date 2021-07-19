import pandas as pd
import pytest

from trade.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from trade.storage.models.security import Security


class TestSecuritiesUpsertStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesUpsertStep

    @pytest.fixture
    def input(self):
        return {
            "symbol": "AAPL",
            "quote_type": "EQUITY",
            "sector": "Technology",
            "country": "United States",
            "industry": "Consumer Electronics",
            "currency": "USD",
            "exchange": "NMS",
            "short_name": "Apple Inc.",
            "long_name": "Apple Inc.",
        }

    def test_persists_new_ticker(self, subject, input):
        result = subject.process([input])

        assert result.is_ok()
        assert result.value[0].symbol == "AAPL"
        assert result.value[0].exchange == "NMS"
        assert isinstance(result.value[0], Security)
