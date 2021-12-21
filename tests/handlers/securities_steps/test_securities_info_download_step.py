import pytest
from result import Ok, Err

from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.storage.data_objects.security_dto import SecurityDTO


class TestSecuritiesInfoDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesInfoDownloadStep

    @pytest.fixture
    def security_dto(self):
        return SecurityDTO(
            symbol="AAAA",
        )

    def test_returns_collection(
        self, subject, security_dto, mock_external_info_requests
    ):
        result = subject().process([security_dto])

        mock_external_info_requests.assert_called_once_with("AAAA")
        assert isinstance(result, Ok)
        assert isinstance(result.value, list)

    def test_error_on_download(
        self, subject, mocker, security_dto, mock_external_info_requests
    ):
        mock_external_info_requests.side_effect = Exception(
            "failed to load because of reason"
        )

        result = subject().process([security_dto])

        assert isinstance(result, Err)
        assert (
            result.err()[0]
            == "Failed to load ticker <AAAA>: failed to load because of reason"
        )
