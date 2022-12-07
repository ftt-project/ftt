import pytest

from ftt.handlers.order_update_handler import OrderUpdateHandler
from ftt.storage.value_objects import OrderValueObject
from ftt.storage.models import Order
from tests.helpers import reload_record


class TestOrderUpdateHandler:
    @pytest.fixture
    def subject(self):
        return OrderUpdateHandler()

    def test_handle_returns_updated_order(self, subject, order):
        dto = OrderValueObject(
            status=Order.Status.COMPLETED,
            execution_size=18,
        )
        result = subject.handle(order_id=order.id, dto=dto)

        assert result.is_ok()
        assert result.value.status == Order.Status.COMPLETED
        assert reload_record(order.weight).position == dto.execution_size
