from trade.storage.models import Ticker, PortfolioVersion, Order


class TestOrder:
    def test_table(self):
        assert Order._meta.table_name == "orders"

    def test_relations(self):
        assert Order.ticker.rel_model == Ticker
        assert Order.portfolio_version.rel_model == PortfolioVersion
