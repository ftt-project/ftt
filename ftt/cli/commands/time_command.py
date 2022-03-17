from datetime import datetime

from nubia import command

from ftt.brokers.utils import build_brokerage_service


def config():
    from collections import namedtuple

    dictionary = {"host": "127.0.0.1", "port": 7497, "client_id": 1234}
    return namedtuple("Config", dictionary.keys())(*dictionary.values())


@command
def time():
    """
    Returns time on IB server
    """
    brokerage_service = build_brokerage_service("Interactive Brokers")
    server_time = brokerage_service.obtain_server_time()

    server_time_readable = datetime.utcfromtimestamp(server_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("Current IB server time: %s" % server_time_readable)


@command
def open_position():
    """
    Return open positions in brokerage system
    """

    brokerage_service = build_brokerage_service("Interactive Brokers", config())
    open_positions = brokerage_service.open_positions()

    print(open_positions)


@command
def place_order():
    from ftt.brokers.contract import Contract
    from ftt.brokers.order import Order

    brokerage_service = build_brokerage_service("Interactive Brokers", config())
    contract = Contract(
        symbol="SHOP",
        security_type="STK",
        exchange="SMART",
        currency="USD",
    )
    order = Order(
        action="BUY",
        total_quantity=1.0,
        order_type="MKT",
    )

    order_id = brokerage_service.place_order(contract, order)
    print(order_id)

    open_orders = brokerage_service.open_orders()
    print(open_orders)
