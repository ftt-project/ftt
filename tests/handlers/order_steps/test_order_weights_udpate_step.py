import pytest

from ftt.handlers.order_steps.order_weights_udpate_step import OrderWeightsUpdateStep
from ftt.storage.value_objects import OrderValueObject


class TestOrderWeightsUpdateStep:
    @pytest.fixture
    def subject(self):
        return OrderWeightsUpdateStep

    def test_process_returns_updated_weight(self, subject, order, security, weight):
        dto = OrderValueObject(execution_size=78)
        result = subject.process(order, dto)

        assert result.is_ok()
        assert result.value.position == 78
