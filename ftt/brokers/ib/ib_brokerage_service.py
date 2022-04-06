import threading

from ftt.brokers.ib.ib_client import IBClient
from ftt.brokers.ib.ib_wrapper import IBWrapper


class IBBrokerageService(IBWrapper, IBClient):
    """
    Implementation of Interactive Brokers service class
    """

    provider_name = "Interactive Brokers"

    def __init__(self, ipaddress, port_id, client_id):
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)

        self.connect(ipaddress, port_id, client_id)

        thread = threading.Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)
