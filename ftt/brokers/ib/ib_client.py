import queue

from ibapi.client import EClient
from ibapi.wrapper import Contract as IBContract
from ibapi.order import Order as IBOrder

from ftt.brokers.contract import Contract
from ftt.brokers.order import Order
from ftt.brokers.position import Position


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

    def obtain_server_time(self):
        """
        Requests the current server time from IB then
        returns it if available.

        Returns
        -------
        `int`
            The server unix timestamp.
        """
        # Instantiate a queue to store the server time
        time_queue = self.wrapper.time()

        # Ask IB for the server time using the EClient method
        self.reqCurrentTime()

        # Try to obtain the latest server time if it exists
        # in the queue, otherwise issue a warning
        try:
            server_time = time_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            print(
                "Time queue was empty or exceeded maximum timeout of "
                "%d seconds" % IBClient.MAX_WAIT_TIME_SECONDS
            )
            server_time = None

        # Output all additional errors, if they exist
        while self.wrapper.is_error():
            print(self.get_error())

        return server_time

    def open_positions(self):
        """
        Returns open positions

        Returns
        -------
        `list` of `Position`
            The open positions for this client.
        """
        open_positions_done_queue = self.wrapper.open_positions()

        self.reqPositions()

        try:
            positions = open_positions_done_queue.get(
                timeout=IBClient.MAX_WAIT_TIME_SECONDS
            )
        except queue.Empty:
            print(
                "Time queue was empty or exceeded maximum timeout of "
                "%d seconds" % IBClient.MAX_WAIT_TIME_SECONDS
            )
            positions = None

        while self.wrapper.is_error():
            print(self.get_error())

        return positions

    def next_valid_id(self, n=1):
        """
        Requests and returns the next valid id for order that is unique for this client.

        Returns
        -------
        `id`
            The next valid id
        """
        id_queue = self.wrapper.next_valid_id()

        self.reqIds(n)

        try:
            next_valid_id = id_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            print(
                "Time queue was empty or exceeded maximum timeout of "
                "%d seconds" % IBClient.MAX_WAIT_TIME_SECONDS
            )
            next_valid_id = None

        while self.wrapper.is_error():
            print(self.get_error())

        return next_valid_id

    def place_order(self, contract: Contract, order: Order) -> int:
        """
        Places order asynchronously according to given contact and order

        Parameters
        ----------
        `contract`
            Contract instance
        `order`
            Order instance

        Returns
        -------
        `id`
            id of the order
        """
        next_order_id = self.next_valid_id()

        ibcontract = IBContract()
        ibcontract.symbol = contract.symbol
        ibcontract.secType = contract.security_type
        ibcontract.exchange = contract.exchange
        ibcontract.currency = contract.currency

        iborder = IBOrder()
        iborder.action = order.action
        iborder.totalQuantity = order.total_quantity
        iborder.orderType = order.order_type

        super().placeOrder(next_order_id, ibcontract, iborder)

        return next_order_id

    def open_orders(self):
        open_orders_queue = self.wrapper.open_orders()

        self.reqOpenOrders()

        try:
            open_orders = open_orders_queue.get(timeout=IBClient.MAX_WAIT_TIME_SECONDS)
        except queue.Empty:
            print(
                "Time queue was empty or exceeded maximum timeout of "
                "%d seconds" % IBClient.MAX_WAIT_TIME_SECONDS
            )
            open_orders = None

        while self.wrapper.is_error():
            print(self.get_error())

        return open_orders
