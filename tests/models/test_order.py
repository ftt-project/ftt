from trade.storage.models import Security, PortfolioVersion, Order


class TestOrder:
    def test_table(self):
        assert Order._meta.table_name == "orders"

    def test_relations(self):
        assert Order.security.rel_model == Security
        assert Order.portfolio_version.rel_model == PortfolioVersion
