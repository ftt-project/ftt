from ftt.storage.models import Portfolio
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security


class TestOrder:
    def test_table(self):
        assert Order._meta.table_name == "orders"

    def test_relations(self):
        assert Order.security.rel_model == Security
        assert Order.portfolio_version.rel_model == PortfolioVersion
        assert Order.portfolio.rel_model == Portfolio
