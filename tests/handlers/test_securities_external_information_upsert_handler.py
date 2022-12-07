import pytest

from ftt.handlers.securities_external_information_upsert_handler import (
    SecuritiesExternalInformationUpsertHandler,
)
from ftt.storage import schemas


class TestSecuritiesExternalInformationUpsertHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesExternalInformationUpsertHandler()

    def test_process(self, subject, mock_external_info_requests, schema_security):
        result = subject.handle(securities=[schema_security])

        mock_external_info_requests.assert_called_once_with("AA.XX")
        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.Security)
        assert result.value[0].symbol == schema_security.symbol
        assert result.value[0].id is not None
