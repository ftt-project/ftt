from datetime import datetime

from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"

    def test_relations(self):
        assert Portfolio.versions.rel_model == PortfolioVersion

    def test_deleted_at_is_not_set_by_default(self):
        assert Portfolio().deleted_at is None
        assert (
            Portfolio.create(name="test", updated_at=datetime.now()).deleted_at is None
        )
