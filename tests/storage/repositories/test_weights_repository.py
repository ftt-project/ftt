from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.storage.models import Weight
from trade.storage.repositories import SecuritiesRepository
from trade.storage.repositories import PortfolioVersionsRepository
from trade.storage.repositories import PortfoliosRepository
from trade.storage.repositories import WeightsRepository


class TestWeightsRepository:
    @fixture
    def subject(self):
        return WeightsRepository()

    @fixture
    def data(self, security, portfolio_version):
        return {
            "portfolio_version": portfolio_version,
            "security": security,
            "planned_position": 2,
            "position": 10
        }

    @fixture
    def weight(self, data):
        data['updated_at'] = datetime.now()
        data['created_at'] = datetime.now()
        return Weight.create(**data)

    def test_create(self, subject, data):
        result = subject.create(data)

        assert type(result) == Weight
        assert result.id is not None

    def test_upsert(self, subject, data, weight):
        result = subject.upsert(data)

        assert result == weight

    def test_get_by_security_and_portfolio_version(self, subject, portfolio_version, security, weight):
        result = subject.get_by_security_and_portfolio_version(
            portfolio_version_id=portfolio_version.id,
            security_id=security.id
        )

        assert result == weight

    def test_find_by_security_and_portfolio(self, subject, security, portfolio_version, weight):
        result = subject.find_by_security_and_portfolio(security=security, portfolio_version_id=portfolio_version.id)
        assert result == weight

    def test_update_amount(self, weight, subject):
        subject.update_amount(weight, 101)
        assert Weight.get(weight.id).amount == 101

    def test_lock_weight(self, subject, weight):
        result = subject.lock_weight(weight, 101)
        assert result.locked_at_amount == 101
        assert result.locked_at is not None

    def test_unlock_weight(self, subject, weight):
        result = subject.unlock_weight(weight)
        assert result.locked_at_amount is None
        assert result.locked_at is None

    def test_update_on_sell(self, subject, weight):
        weight.peaked_value = 101
        weight.amount = 1000
        weight.save()

        result = subject.update_on_sell(weight)
        assert 0 == result.amount
        assert 0 == result.peaked_value

    def test_update_on_buy(self, subject, weight):
        result = subject.update_on_buy(weight, 89)
        assert 89 == result.amount
