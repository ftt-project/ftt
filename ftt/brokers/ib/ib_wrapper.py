import queue
from datetime import datetime
from decimal import Decimal

from ibapi.wrapper import EWrapper, Contract as IBContract
from ibapi.common import OrderId
from ibapi.order import Order
from ibapi.order_state import OrderState

from ftt.brokers.position import Position
from ftt.handlers.order_update_handler import OrderUpdateHandler
from ftt.logger import Logger
from ftt.storage.data_objects.order_dto import OrderDTO


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
        self._next_valid_id_queue = queue.Queue()
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
        error_message = (
            f"IB Error ID {id}, Error Code {errorCode} with "
            f"response '{errorString}'"
        )
        self._errors.put(error_message)

    def time_queue(self) -> queue.Queue:
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

    def open_positions_queue(self) -> queue.Queue:
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

    def open_orders_queue(self) -> queue.Queue:
        """
        Returns a final queue with all open orders that are received asynchronously
        (see `openOrder` and `openOrderEnd`)

        Returns
        -------
        `Queue`
            A final queue for all open orders.
        """
        return self._open_orders_done_queue

    def next_valid_id_queue(self) -> queue.Queue:
        """
        Returns queue with the next valid id.
        """
        return self._next_valid_id_queue

    def currentTime(self, server_time):
        """
        Takes the time received by the server and
        appends it to the class instance time queue.

        Parameters
        ----------
        server_time : `str`
            The server time message.
        """
        self._time_queue.put(server_time)

    def nextValidId(self, order_id: int):
        """
        Is callback that stores the next valid id received from the server.
        """
        Logger.info(f"{__name__}::nextValidId Next valid order id is {order_id}")
        self._next_valid_id_queue.put(order_id)

    def position(
        self, account: str, contract: IBContract, position: Decimal, avg_cost: float
    ) -> None:
        """
        This method receives open positions from IB, maps them into `ib.Position` object, and puts into the
        `_open_positions_queue` queue to be retrieved in `positionEnd` callback.

        See https://interactivebrokers.github.io/tws-api/positions.html
        """
        Logger.info(
            f"{__name__}::position: {account}, {contract}, {position}, {avg_cost}"
        )
        self._open_positions_queue.put(
            Position(
                account=account,
                contract=contract,
                position=float(position),
                avg_cost=avg_cost,
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

    def connectionClosed(self):
        Logger.info(f"{__name__}::connectionClosed")

    def orderStatus(
        self,
        order_id: OrderId,
        status: str,
        filled: float,
        remaining: float,
        avg_fill_price: float,
        perm_id: int,
        parent_id: int,
        last_fill_price: float,
        client_id: int,
        why_held: str,
        mkt_cap_price: float,
    ):

        Logger.info(
            f"{__name__}::orderStatus: Received order_id:{order_id} status:{status}"
            f"filled:{filled} remaining:{remaining} avg_fill_price:{avg_fill_price}"
            f"perm_id:{perm_id} parent_id:{parent_id} last_fill_price:{last_fill_price}"
        )

        dto = OrderDTO(
            status=status,
            execution_size=filled,
            execution_price=avg_fill_price,
            executed_at=datetime.now(),
        )

        # TODO it must update weights in the portfolio according to the filled size
        result = OrderUpdateHandler().handle(order_id=order_id, dto=dto)

        if result.is_ok():
            Logger.info(
                f"{__name__}::orderStatus: updated order_id: {order_id} status: {status}"
            )
        else:
            Logger.error(
                f"{__name__}::orderStatus: failed to update order_id: {order_id} with error: {result.error}"
            )
