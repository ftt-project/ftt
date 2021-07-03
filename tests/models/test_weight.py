from trade.storage.models import Weight, PortfolioVersion, Security


class TestWeight:
    def test_table(self):
        assert Weight._meta.table_name == "weights"

    def test_relations(self):
        assert Weight.portfolio_version.rel_model == PortfolioVersion
        assert Weight.security.rel_model == Security
