from trade.services.exchange_name_normalizer import ExchangeNameNormalizer


class TestExchangeNameNormalizer:
    def test_tor(self):
        assert "Toronto" == ExchangeNameNormalizer("TOR").perform()

    def test_ncm(self):
        assert "NASDAQ" == ExchangeNameNormalizer("NCM").perform()

    def test_nyq(self):
        assert "NYSE" == ExchangeNameNormalizer("NYQ").perform()

    def test_default_value(self):
        assert "ABC" == ExchangeNameNormalizer("ABC").perform()