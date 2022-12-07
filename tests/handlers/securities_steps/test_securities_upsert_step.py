import pytest

from ftt.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from ftt.storage import schemas


class TestSecuritiesUpsertStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesUpsertStep

    def test_persists_new_ticker(self, subject, schema_security):
        assert schema_security.id is None

        result = subject.process([schema_security])

        assert result.is_ok()
        assert result.value[0].id is not None
        assert result.value[0].symbol == schema_security.symbol
        assert result.value[0].exchange == schema_security.exchange
        assert isinstance(result.value[0], schemas.Security)
