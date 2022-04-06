import pytest

from ftt.handlers.order_steps.order_load_step import OrderLoadStep


class TestOrderLoadStep:
    @pytest.fixture
    def subject(self):
        return OrderLoadStep

    def test_process_returns_order_by_id(self, subject, order):
        result = subject.process(order.id)

        assert result.is_ok()
        assert result.value == order
