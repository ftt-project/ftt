import queue

from ibapi.client import EClient


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
        time_queue = self.wrapper.init_time()

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
