from trade.storage.models import Ticker, Order


class TestTicker:
    def test_table(self):
        assert Ticker._meta.table_name == "tickers"

    def test_relations(self):
        assert Ticker.orders.rel_model == Order
