from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.models.security import Security
from trade.storage.models.weight import Weight


class TestWeight:
    def test_table(self):
        assert Weight._meta.table_name == "weights"

    def test_relations(self):
        assert Weight.portfolio_version.rel_model == PortfolioVersion
        assert Weight.security.rel_model == Security
