from datetime import datetime
import peewee
import pytest

from trade.models import Portfolio, PortfolioVersion


class TestPortfolio:
    def test_table_name(self):
        assert Portfolio._meta.table_name == "portfolios"

    def test_relations(self):
        assert Portfolio.versions.rel_model == PortfolioVersion

    def test_size_constraints(self):
        with pytest.raises(peewee.IntegrityError) as e:
            Portfolio.create(name='test', amount=-1, updated_at=datetime.now(), created_at=datetime.now())

        assert 'new row for relation "portfolios" violates check constraint "portfolios_amount_check' in str(e.value)

    def test_size_default_value(self):
        portfolio = Portfolio.create(name='test', amount=1, updated_at=datetime.now(), created_at=datetime.now())
        portfolio.amount = -1
        with pytest.raises(peewee.IntegrityError) as e:
            portfolio.save()

        assert 'new row for relation "portfolios" violates check constraint "portfolios_amount_check' in str(e.value)
