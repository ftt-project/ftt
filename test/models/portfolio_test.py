from trade.db.portfolio import Portfolio


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"
