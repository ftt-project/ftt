from datetime import datetime

import peewee
import pytest

from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
)
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion


class TestPortfolioVersion:
    def test_table(self):
        assert PortfolioVersion._meta.table_name == "portfolio_versions"

    def test_relations(self):
        assert PortfolioVersion.portfolio.rel_model == Portfolio
        assert PortfolioVersion.orders.rel_model == Order

    def test_amount_default_value(self, portfolio):
        portfolio = PortfolioVersion.create(
            portfolio=portfolio,
            version=1,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

        assert portfolio.value == 0

    def test_amount_constraints(self, portfolio):
        with pytest.raises(peewee.IntegrityError) as e:
            PortfolioVersion.create(
                portfolio=portfolio,
                version=1,
                value=-1,
                optimization_strategy_name=OptimizationStrategyResolver.strategies()[0],
                updated_at=datetime.now(),
                created_at=datetime.now(),
            )

        assert "CHECK constraint failed" in str(e.value)
