import queue
from typing import Union, Optional

from ibapi.client import EClient
from ibapi.wrapper import Contract as IBContract
from ibapi.order import Order as IBOrder

from ftt.logger import Logger
from ftt.brokers.contract import Contract
from ftt.brokers.broker_order import BrokerOrder


class IBClient(EClient):
    """
    Used to send messages to the IB servers via the API. In this
    simple derived subclass of EClient we provide a method called
    obtain_server_time to carry out a 'sanity check' for connection
    testing.

    Parameters
    ----------
    wrapper : `EWrapper` derived subclass
        Used to handle the responses sent from IB servers
    """

    MAX_WAIT_TIME_SECONDS = 10

    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def server_time(self):
        """
        Requests the current server time from IB then
        returns it if available.

        Returns
        -------
        `int`
            The server unix timestamp.
        """
        # Instantiate a queue to store the server time
        time_queue = self.wrapper.time_queue()

        # Ask IB for the server time using the EClient method
        self.reqCurrentTime()

        # Try to obtain the latest server time if it exists
        # in the queue, otherwise issue a warning
        try:
            server_time = time_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            print(
                f"{__name__}::server_time Time queue was empty or exceeded maximum timeout of "
                f"{IBClient.MAX_WAIT_TIME_SECONDS} seconds"
            )
            server_time = None

        # Output all additional errors, if they exist
        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        return server_time

    def open_positions(self) -> list:
        """
        Returns open positions

        Returns
        -------
        `list` of `Position`
            The open positions for this client.
        """
        open_positions_done_queue = self.wrapper.open_positions_queue()

        self.reqPositions()

        try:
            positions = open_positions_done_queue.get(
                timeout=IBClient.MAX_WAIT_TIME_SECONDS
            )
        except queue.Empty:
            Logger.error(
                f"{__name__}::open_positions queue was empty or exceeded maximum timeout of "
                f"{IBClient.MAX_WAIT_TIME_SECONDS} seconds"
            )
            positions = None

        while self.wrapper.is_error():
            Logger.error(f"{__name__}::open_positions {self.wrapper.get_error()}")
            positions = None

        return positions

    def next_valid_id(self):
        """
        Requests and returns the next valid id for order that is unique for this client.

        Returns
        -------
        `id`
            The next valid id
        """
        id_queue = self.wrapper.next_valid_id_queue()

        self.reqIds(-1)

        try:
            next_valid_id = id_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            Logger.error(
                f"{__name__}::next_valid_id queue was empty or exceeded maximum timeout of "
                f"{IBClient.MAX_WAIT_TIME_SECONDS} seconds"
            )
            next_valid_id = None

        while self.wrapper.is_error():
            Logger.error(f"{__name__}::next_valid_id {self.wrapper.get_error()}")
            return None

        return next_valid_id

    def place_order(
        self,
        contract: Contract,
        order: BrokerOrder,
        next_order_id: Optional[int] = None,
    ) -> Union[int, None]:
        """
        Places order asynchronously according to given contact and order

        Parameters
        ----------
        `contract`
            Contract instance
        `order`
            Order instance
        `next_order_id`
            Optional order id. If it is not given then the next valid id is requested and used.

        Returns
        -------
        `id`
            id of the order
        """
        if next_order_id is None:
            next_order_id = self.next_valid_id()

        if next_order_id is None:
            Logger.error(f"{__name__}::place_order failed to get next valid id")
            return None

        ibcontract = IBContract()
        ibcontract.symbol = contract.symbol
        ibcontract.secType = contract.security_type
        ibcontract.exchange = contract.exchange
        ibcontract.currency = contract.currency

        iborder = IBOrder()
        iborder.action = order.action.value
        iborder.totalQuantity = order.total_quantity
        iborder.orderType = order.order_type.value

        super().placeOrder(next_order_id, ibcontract, iborder)

        return next_order_id

    def open_orders(self):
        open_orders_queue = self.wrapper.open_orders_queue()

        self.reqOpenOrders()

        try:
            open_orders = open_orders_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            Logger.error(
                f"{__name__}::open_orders queue was empty or exceeded maximum timeout of "
                f"{IBClient.MAX_WAIT_TIME_SECONDS} seconds"
            )
            open_orders = None

        while self.wrapper.is_error():
            Logger.error(f"{__name__}::open_orders {self.wrapper.get_error()}")
            open_orders = None

        return open_orders
