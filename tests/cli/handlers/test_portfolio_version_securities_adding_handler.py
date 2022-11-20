import pytest
from pandas import DataFrame

from ftt.handlers.portfolio_version_securities_adding_handler import (
    PortfolioVersionSecuritiesAddingHandler,
)
from ftt.storage.data_objects.security_dto import SecurityValueObject
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class TestPortfolioVersionSecuritiesAddingHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionSecuritiesAddingHandler()

    @pytest.fixture
    def securities_dtos_list(self):
        return [
            SecurityValueObject(
                symbol="AAPL",
                quote_type="EQUITY",
                sector="Technology",
                country="United States",
                industry="Consumer Electronics",
                currency="USD",
                exchange="NMS",
                short_name="Apple Inc.",
                long_name="Apple Inc.",
            )
        ]

    @pytest.fixture(autouse=True)
    def mock_external_info_requests(self, mocker):
        mock = mocker.patch("yfinance.Ticker")
        mock.return_value.info = {
            "symbol": "AAPL",
            "exchange": "NMS",
            "quoteType": "stock",
            "shortName": "Apple Inc.",
            "longName": "Apple Inc.",
        }

    @pytest.fixture(autouse=True)
    def mock_external_historic_data_requests(self, mocker):
        mocker.patch("yfinance.pdr_override")
        mock = mocker.patch("pandas_datareader.data.get_data_yahoo")
        mock.return_value = DataFrame()

    def test_associates_securities_with_portfolio_version(
        self, subject, portfolio_version, portfolio, securities_dtos_list
    ):
        result = subject.handle(
            portfolio_version_id=portfolio_version.id, securities=securities_dtos_list
        )

        assert result.is_ok()

        result = SecuritiesRepository.find_securities(
            portfolio_version=portfolio_version
        )
        assert len(result) == 1
        assert result[0].symbol == securities_dtos_list[0].symbol
