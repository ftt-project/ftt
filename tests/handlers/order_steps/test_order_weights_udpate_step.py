import pytest

from ftt.handlers.order_steps.order_weights_udpate_step import OrderWeightsUpdateStep
from ftt.storage.data_objects.order_dto import OrderDTO


class TestOrderWeightsUpdateStep:
    @pytest.fixture
    def subject(self):
        return OrderWeightsUpdateStep

    def test_process_returns_updated_weight(self, subject, order, security, weight):
        dto = OrderDTO(execution_size=78)
        result = subject.process(order, dto)

        assert result.is_ok()
        assert result.value.position == 78
