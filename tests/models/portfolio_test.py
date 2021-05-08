from trade.models import Portfolio, PortfolioVersion


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"

    def test_relations(self):
        assert Portfolio.versions.rel_model == PortfolioVersion
