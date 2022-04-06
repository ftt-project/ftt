from ftt.brokers.broker_order import BrokerOrder
from ftt.brokers.contract import Contract


class BrokerageService:
    """
    This class follows Bridge pattern abstracting concrete brokerage service implementation.
    """

    def __init__(self, impl):
        self._implementation = impl

    @property
    def provider_name(self):
        return self._implementation.provider_name

    def open_positions(self):
        return self._implementation.open_positions()

    def server_time(self):
        return self._implementation.server_time()

    def next_valid_id(self):
        return self._implementation.next_valid_id()

    def place_order(self, contract: Contract, order: BrokerOrder):
        return self._implementation.place_order(contract, order)

    def open_orders(self):
        return self._implementation.open_orders()
