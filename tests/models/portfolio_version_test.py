from trade.storage.models import PortfolioVersion, Portfolio, Order


class TestPortfolioVersion:
    def test_table(self):
        assert PortfolioVersion._meta.table_name == "portfolio_versions"

    def test_relations(self):
        assert PortfolioVersion.portfolio.rel_model == Portfolio
        assert PortfolioVersion.orders.rel_model == Order
