from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolioVersion:
    def test_table(self):
        assert PortfolioVersion._meta.table_name == "portfolio_versions"

    def test_relations(self):
        assert PortfolioVersion.portfolio.rel_model == Portfolio
        assert PortfolioVersion.orders.rel_model == Order
