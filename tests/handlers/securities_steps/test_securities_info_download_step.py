import pytest
from result import Ok, Err

from trade.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)


class TestSecuritiesInfoDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesInfoDownloadStep

    def test_returns_collection(self, subject, mocker):
        mock = mocker.patch("yfinance.Ticker")
        result = subject().process(["AAAA"])

        mock.assert_called_once_with("AAAA")
        assert isinstance(result, Ok)
        assert isinstance(result.value, list)

    def test_error_on_downlaod(self, subject, mocker):
        mock = mocker.patch("yfinance.Ticker")
        mock.side_effect = Exception("failed to load because of reason")

        result = subject().process(["AAAA"])

        assert isinstance(result, Err)
        assert (
            result.err()[0]
            == "Failed to load ticker <AAAA>: failed to load because of reason"
        )
