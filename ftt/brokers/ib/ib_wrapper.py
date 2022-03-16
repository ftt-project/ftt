import queue
from decimal import Decimal

from ibapi.wrapper import EWrapper, Contract as IBContract
from ibapi.common import OrderId
from ibapi.order import Order
from ibapi.order_state import OrderState

from ftt.brokers.position import Position


class IBWrapper(EWrapper):
    """
    A derived subclass of the IB API EWrapper interface
    that allows more straightforward response processing
    from the IB Gateway or an instance of TWS.
    """

    def __init__(self):
        self._open_positions_queue = queue.Queue()
        self._open_positions_done_queue = queue.Queue()
        self._open_orders_queue = queue.Queue()
        self._open_orders_done_queue = queue.Queue()
        self._next_valid_id = queue.Queue()
        self._time_queue = queue.Queue()
        self._errors = queue.Queue()

    def is_error(self):
        """
        Check the error queue for the presence
        of errors.

        Returns
        -------
        `boolean`
            Whether the error queue is not empty
        """
        return not self._errors.empty()

    def get_error(self, timeout=5):
        """
        Attempts to retrieve an error from the error queue,
        otherwise returns None.

        Parameters
        ----------
        timeout : `float`
            Time-out after this many seconds.

        Returns
        -------
        `str` or None
            A potential error message from the error queue.
        """
        if self.is_error():
            try:
                return self._errors.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(self, id, errorCode, errorString):
        """
        Format the error message with appropriate codes and
        place the error string onto the error queue.
        """
        error_message = "IB Error ID (%d), Error Code (%d) with " "response '%s'" % (
            id,
            errorCode,
            errorString,
        )
        self._errors.put(error_message)

    def time(self) -> queue.Queue:
        """
        Instantiates a new queue to store the server
        time, assigning it to a 'private' instance
        variable and also returning it.

        Returns
        -------
        `Queue`
            The time queue instance.
        """
        return self._time_queue

    def open_positions(self) -> queue.Queue:
        """
        Returns a final queue with all open positions that are received asynchronously
        (see `position` and `positionEnd`), and the second queue that returns all received open
        positions as one list when receiving is completed (see `positionEnd`)

        Returns
        -------
        `Queue`
            The open positions queue instance.
        """
        return self._open_positions_done_queue

    def open_orders(self) -> queue.Queue:
        """
        Returns a final queue with all open orders that are received asynchronously
        (see `openOrder` and `openOrderEnd`)

        Returns
        -------
        `Queue`
            A final queue for all open orders.
        """
        return self._open_orders_done_queue

    def next_valid_id(self) -> queue.Queue:
        """
        Returns queue with the next valid id.
        """
        return self._next_valid_id

    def currentTime(self, server_time) -> str:
        """
        Takes the time received by the server and
        appends it to the class instance time queue.

        Parameters
        ----------
        server_time : `str`
            The server time message.
        """
        self._time_queue.put(server_time)

    def nextValidId(self, order_id: int) -> None:
        """
        Is callback that stores the next valid id received from the server.
        """
        self._next_valid_id.put(order_id)

    def position(
        self, account: str, contract: IBContract, position: Decimal, avg_cost: float
    ) -> None:
        """
        This method receives open positions from IB, maps them into `ib.Position` object, and puts into the
        `_open_positions_queue` queue to be retrieved in `positionEnd` callback.

        See https://interactivebrokers.github.io/tws-api/positions.html
        """
        self._open_positions_queue.put(
            Position(
                account=account, contract=contract, position=position, avg_cost=avg_cost
            )
        )

    def positionEnd(self) -> None:
        """
        See `position` method.
        See https://interactivebrokers.github.io/tws-api/positions.html
        """
        self._open_positions_done_queue.put(list(self._open_positions_queue.queue))

    def openOrder(
        self,
        order_id: OrderId,
        contract: IBContract,
        order: Order,
        order_state: OrderState,
    ):
        self._open_orders_queue.put(
            {
                "order_id": order_id,
                "contract": contract,
                "order": order,
                "order_state": order_state,
            }
        )

    def openOrderEnd(self):
        self._open_orders_done_queue.put(list(self._open_orders_queue.queue))
