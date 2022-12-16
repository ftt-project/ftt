from datetime import datetime

import pytest
from pytest import fixture

from ftt.storage import schemas
from ftt.storage.models.weight import Weight
from ftt.storage.repositories.weights_repository import WeightsRepository


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
            "position": 10,
        }

    @fixture
    def weight(self, data):
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return Weight.create(**data)

    def test_create(self, subject, data):
        result = subject.create(data)

        assert type(result) == Weight
        assert result.id is not None

    def test_upsert(self, subject, data, weight):
        result = subject.upsert(data)

        assert result == weight

    def test_upsert_returns_weight_always(self, subject, data, weight):
        result1 = subject.upsert(data)
        result2 = subject.upsert(data)

        assert result1 == weight
        assert result2 == weight

    def test_get_by_security_and_portfolio_version(
        self, subject, portfolio_version, security, weight
    ):
        result = subject.get_by_security_and_portfolio_version(
            portfolio_version_id=portfolio_version.id, security_id=security.id
        )

        assert result == weight

    def test_find_by_security_and_portfolio(
        self, subject, security, portfolio_version, weight
    ):
        result = subject.find_by_security_and_portfolio(
            security=security, portfolio_version_id=portfolio_version.id
        )
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

    def test_get_by_portfolio_version_returns_list_of_weights(
        self, subject, portfolio_version, weight
    ):
        result = subject.get_by_portfolio_version(
            schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert isinstance(result, list)
        assert isinstance(result[0], schemas.Weight)
        assert result[0].id == weight.id

    def test_delete_returns_true(self, subject, weight):
        result = subject.delete(schemas.Weight(id=weight.id))

        assert result is True
        assert not Weight.select().exists()
        assert Weight.select_deleted().exists()

    def test_delete_not_persisted_record_returns_false(self, subject, weight):
        schema_weight = schemas.Weight(id=weight.id)
        subject.delete(schema_weight, soft_delete=False)
        with pytest.raises(Weight.DoesNotExist) as excinfo:
            subject.delete(weight)

        assert "instance matching query does not exist" in str(excinfo.value)
