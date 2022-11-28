import pytest

from ftt.handlers.securities_information_loading_handler import (
    SecuritiesInformationLoadingHandler,
)
from ftt.storage.value_objects import SecurityValueObject


class TestSecuritiesInformationLoadingHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesInformationLoadingHandler()

    def test_process(self, subject, mock_external_info_requests):
        result = subject.handle(securities=[SecurityValueObject("AAPL")])

        mock_external_info_requests.assert_called_once_with("AAPL")
        assert result.is_ok()
        assert result.value[0]["symbol"] == "AAPL"
