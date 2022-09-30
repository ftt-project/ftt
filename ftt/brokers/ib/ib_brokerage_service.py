import socket
import threading
import time

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
        self.ipaddress = ipaddress
        self.port_id = port_id
        self.client_id = client_id

        # self.establish_connection()

    def establish_connection(self):
        # if self.conn and self.conn.isConnected():
        #     return

        print("Connecting to IB Gateway on %s:%s" % (self.ipaddress, self.port_id))
        self.connect(self.ipaddress, self.port_id, self.client_id)
        print(self.conn.socket)
        thread = threading.Thread(target=self.run)
        thread.start()
        thread.join(1)  # TODO wait 1 sec. wft?
        setattr(self, "_thread", thread)

    def shutdown_and_disconnect(self):
        if not self.conn or not self.conn.isConnected():
            print("Already disconnected")
            self.reset()
            return

        self.conn.lock.acquire()
        try:
            if self.conn.socket is not None:
                print("shutting down socket")
                self.conn.socket.shutdown(socket.SHUT_RDWR)
                time.sleep(1)
        finally:
            print("shutdown_and_disconnect releasing lock")
            self.conn.lock.release()
            self.disconnect()
