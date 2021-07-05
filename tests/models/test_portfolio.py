from datetime import datetime
import peewee
import pytest

from trade.storage.models.portfolio import Portfolio
from trade.storage.models.portfolio_version import PortfolioVersion


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"

    def test_relations(self):
        assert Portfolio.versions.rel_model == PortfolioVersion

    def test_size_constraints(self):
        with pytest.raises(peewee.IntegrityError) as e:
            Portfolio.create(name='test', amount=-1, updated_at=datetime.now(), created_at=datetime.now())

        assert 'CHECK constraint failed' in str(e.value)

    def test_size_default_value(self):
        portfolio = Portfolio.create(name='test', amount=1, updated_at=datetime.now(), created_at=datetime.now())
        portfolio.amount = -1
        with pytest.raises(peewee.IntegrityError) as e:
            portfolio.save()

        assert 'CHECK constraint failed' in str(e.value)
