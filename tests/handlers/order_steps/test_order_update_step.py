import pytest

from ftt.handlers.order_steps.order_update_step import OrderUpdateStep
from ftt.storage.models import Order


class TestOrderUpdateStep:
    @pytest.fixture
    def subject(self):
        return OrderUpdateStep

    def test_process_updates_order(self, subject, order):
        from ftt.storage.data_objects.order_dto import OrderDTO

        dto = OrderDTO(
            status=Order.Status.PARTIAL,
        )
        result = subject.process(order, dto)

        assert result.is_ok()
        assert order.status == Order.Status.PARTIAL
