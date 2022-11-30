import pytest

from ftt.handlers.securities_information_loading_handler import (
    SecuritiesInformationLoadingHandler,
)
from ftt.storage import schemas
from ftt.storage.value_objects import SecurityValueObject


class TestSecuritiesInformationLoadingHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesInformationLoadingHandler()

    def test_process(self, subject, mock_external_info_requests, schema_security):
        result = subject.handle(securities=[schema_security])

        mock_external_info_requests.assert_called_once_with("AA.XX")
        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.Security)
        assert result.value[0].symbol == schema_security.symbol
        assert result.value[0].id is not None
