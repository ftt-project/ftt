from datetime import datetime

import pytest

from trade.handlers.securities_steps.securities_load_prices_step import SecuritiesLoadPricesStep


class TestSecuritiesLoadPriceStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesLoadPricesStep

    def test_load_securities_historical_prices(self, subject, mocker, security):
        mocker.patch("yfinance.pdr_override")
        mock = mocker.patch('pandas_datareader.data.get_data_yahoo')
        mock.return_value = 'pandas result'
        result = subject.process(
            securities=[security],
            period_from=datetime.today(),
            period_to=datetime.today(),
            interval='1d'
        )

        mock.assert_called_once()
        assert result.is_ok()
        assert result.value == {security.symbol: "pandas result"}
