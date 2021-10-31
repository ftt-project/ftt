from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"

    def test_relations(self):
        assert Portfolio.versions.rel_model == PortfolioVersion
