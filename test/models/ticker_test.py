from trade.db.ticker import Ticker


class TestTicker:
    def test_table(self):
        assert Ticker._meta.table_name == "tickers"
