from ftt.storage.models import Security
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_security import PortfolioSecurity


class TestPortfolioSecurity:
    def test_table_name(self):
        assert PortfolioSecurity._meta.table_name == "portfolio_securities"

    def test_relations(self):
        assert PortfolioSecurity.portfolio.rel_model == Portfolio
        assert PortfolioSecurity.security.rel_model == Security
