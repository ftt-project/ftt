import queue

import pytest

from ftt.brokers.ib.ib_client import IBClient


class TestIBClient:
    @pytest.fixture
    def subject(self, wrapper):
        return IBClient(wrapper)

    @pytest.fixture
    def wrapper(self, mocker):
        wrapper = mocker.MagicMock()
        wrapper.is_error.return_value = False
        return wrapper

    def test_open_positions_returns_open_positions(self, subject, wrapper, mocker):
        wrapper.open_positions_queue.return_value.get.return_value = (
            mocker.sentinel.result
        )
        reqPositions = mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqPositions")

        result = subject.open_positions()

        assert result == mocker.sentinel.result
        assert reqPositions.call_count == 1

    def test_open_positions_log_error_on_timeout(self, subject, wrapper, mocker):
        wrapper.open_positions_queue.return_value.get.side_effect = queue.Empty
        mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqPositions")
        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.open_positions()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::open_positions queue was empty or exceeded maximum "
            "timeout of 10 seconds"
        )

    def test_open_positions_log_error_on_wrapper_error(self, subject, wrapper, mocker):
        wrapper.open_positions_queue.return_value.get.return_value = []
        wrapper.is_error.side_effect = [True, False]
        wrapper.get_error.return_value = mocker.sentinel.error

        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.open_positions()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::open_positions sentinel.error"
        )

    def test_next_valid_id_returns_next_valid_id(self, subject, wrapper, mocker):
        wrapper.next_valid_id_queue.return_value.get.return_value = (
            mocker.sentinel.result
        )
        reqIds = mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqIds")

        result = subject.next_valid_id()

        assert result == mocker.sentinel.result
        assert reqIds.call_count == 1

    def test_next_valid_id_log_error_on_timeout(self, subject, wrapper, mocker):
        wrapper.next_valid_id_queue.return_value.get.side_effect = queue.Empty
        mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqIds")
        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.next_valid_id()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::next_valid_id queue was empty or exceeded maximum "
            "timeout of 10 seconds"
        )

    def test_next_valid_id_log_error_on_wrapper_error(self, subject, wrapper, mocker):
        wrapper.next_valid_id_queue.return_value.get.return_value = []
        wrapper.is_error.side_effect = [True, False]
        wrapper.get_error.return_value = mocker.sentinel.error

        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.next_valid_id()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::next_valid_id sentinel.error"
        )

    def test_place_order_returns_external_order_id(self, subject, wrapper, mocker):
        mocker.patch(
            "ftt.brokers.ib.ib_client.IBClient.next_valid_id",
            return_value=mocker.sentinel.order_id,
        )
        placeOrder = mocker.patch("ftt.brokers.ib.ib_client.EClient.placeOrder")

        result = subject.place_order(mocker.MagicMock(), mocker.MagicMock())

        assert result == mocker.sentinel.order_id
        placeOrder.assert_called_once()

    def test_place_order_id_with_given_next_order_id(self, subject, wrapper, mocker):
        mocker.patch(
            "ftt.brokers.ib.ib_client.IBClient.next_valid_id",
            return_value=mocker.sentinel.order_id,
        )
        placeOrder = mocker.patch("ftt.brokers.ib.ib_client.EClient.placeOrder")

        result = subject.place_order(mocker.MagicMock(), mocker.MagicMock(), 129)

        assert result == 129
        placeOrder.assert_called_once()

    def test_place_order_returns_none_if_next_valid_id_none(
        self, subject, wrapper, mocker
    ):
        mocker.patch(
            "ftt.brokers.ib.ib_client.IBClient.next_valid_id", return_value=None
        )
        placeOrder = mocker.patch("ftt.brokers.ib.ib_client.EClient.placeOrder")
        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.place_order(mocker.MagicMock(), mocker.MagicMock())

        assert result is None
        placeOrder.assert_not_called()
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::place_order failed to get next valid id"
        )

    def test_open_orders_returns_open_orders(self, subject, wrapper, mocker):
        wrapper.open_orders_queue.return_value.get.return_value = mocker.sentinel.result
        reqOpenOrders = mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqOpenOrders")

        result = subject.open_orders()

        assert result == mocker.sentinel.result

    def test_open_orders_log_error_on_timeout(self, subject, wrapper, mocker):
        wrapper.open_orders_queue.return_value.get.side_effect = queue.Empty
        mocker.patch("ftt.brokers.ib.ib_client.IBClient.reqOpenOrders")

        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.open_orders()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::open_orders queue was empty or exceeded maximum "
            "timeout of 10 seconds"
        )

    def test_open_orders_log_error_on_wrapper_error(self, subject, wrapper, mocker):
        wrapper.open_orders_queue.return_value.get.return_value = []
        wrapper.is_error.side_effect = [True, False]
        wrapper.get_error.return_value = mocker.sentinel.error

        logger = mocker.patch("ftt.brokers.ib.ib_client.logger")

        result = subject.open_orders()

        assert result is None
        logger.error.assert_called_once_with(
            "ftt.brokers.ib.ib_client::open_orders sentinel.error"
        )
