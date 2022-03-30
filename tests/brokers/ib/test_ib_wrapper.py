import pytest

from ftt.brokers.ib.ib_wrapper import IBWrapper
from ftt.storage.models import Order
from tests.helpers import reload_record


class TestIBWrapper:
    @pytest.fixture
    def subject(self):
        return IBWrapper()

    def test_orderStatus_updates_associated_order(self, subject, order):
        subject.orderStatus(
            order_id=order.id,
            status=Order.Status.ACCEPTED,
            filled=1,
            remaining=0,
            avg_fill_price=1.0,
            perm_id=0,
            parent_id=0,
            last_fill_price=1.0,
            client_id=0,
            why_held='',
            mkt_cap_price=1.0,
        )

        o = reload_record(order)
        assert o.status == Order.Status.ACCEPTED
        assert o.execution_size == 1
        assert o.execution_price == 1.0
        assert o.executed_at is not None
        assert o.weight.position == 1

    def test_orderStatus_log_success_message(self, subject, order, mocker):
        logger = mocker.patch('ftt.brokers.ib.ib_wrapper.logger')
        subject.orderStatus(
            order_id=order.id,
            status=Order.Status.ACCEPTED,
            filled=1,
            remaining=0,
            avg_fill_price=1.0,
            perm_id=0,
            parent_id=0,
            last_fill_price=1.0,
            client_id=0,
            why_held='',
            mkt_cap_price=1.0,
        )

        logger.info.assert_any_call(
            f"ftt.brokers.ib.ib_wrapper::orderStatus: updated order_id: {order.id} status: {Order.Status.ACCEPTED}"
        )

    def test_orderStatus_log_failure_message(self, subject, order, mocker):
        logger = mocker.patch('ftt.brokers.ib.ib_wrapper.logger')
        handler = mocker.patch('ftt.brokers.ib.ib_wrapper.OrderUpdateHandler')
        handler.return_value.handle.return_value.is_ok.return_value = False
        handler.return_value.handle.return_value.error = "Error"

        subject.orderStatus(
            order_id=order.id,
            status=Order.Status.REJECTED,
            filled=0,
            remaining=0,
            avg_fill_price=0.0,
            perm_id=0,
            parent_id=0,
            last_fill_price=0.0,
            client_id=0,
            why_held='',
            mkt_cap_price=0.0,
        )

        logger.error.assert_any_call(
            f"ftt.brokers.ib.ib_wrapper::orderStatus: failed to update order_id: {order.id} with error: Error"
        )

