from datetime import datetime

from nubia import command  # type: ignore

from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.utils import build_brokerage_service


@command
def time():
    """
    Returns time on IB server
    """
    brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig())
    server_time = brokerage_service.server_time()

    server_time_readable = datetime.utcfromtimestamp(server_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("Current IB server time: %s" % server_time_readable)


@command
def open_position():
    """
    Return open positions in brokerage system
    """

    brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig())
    open_positions = brokerage_service.open_positions()

    print(open_positions)


@command
def place_order():
    pass
    # from ftt.brokers.contract import Contract
    # from ftt.brokers.order import Order
    #
    # brokerage_service = build_brokerage_service("Interactive Brokers", config())
    # contract = Contract(
    #     symbol="SHOP",
    #     security_type="STK",
    #     exchange="SMART",
    #     currency="USD",
    # )
    # order = BrokerOrder(
    #     action="BUY",
    #     total_quantity=1.0,
    #     order_type="MKT",
    # )
    #
    # order_id = brokerage_service.place_order(contract, order)
    # print(order_id)
    #
    # open_orders = brokerage_service.open_orders()
    # print(open_orders)
