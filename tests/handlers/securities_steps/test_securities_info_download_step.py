import pytest
from result import Ok, Err

from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.storage import schemas
from ftt.storage.value_objects import SecurityValueObject


class TestSecuritiesInfoDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesInfoDownloadStep

    def test_returns_collection(
        self, subject, mock_external_info_requests, schema_security
    ):
        result = subject().process([schema_security])

        mock_external_info_requests.assert_called_once_with(schema_security.symbol)
        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.Security)

    def test_error_on_download(
        self, subject, schema_security, mock_external_info_requests
    ):
        mock_external_info_requests.side_effect = Exception(
            "failed to load because of reason"
        )

        result = subject().process([schema_security])

        assert result.is_err()
        assert (
            result.err()[0]
            == "Failed to load ticker <AA.XX>: failed to load because of reason"
        )
