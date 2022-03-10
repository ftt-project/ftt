import queue

from ibapi.wrapper import EWrapper


class IBWrapper(EWrapper):
    """
    A derived subclass of the IB API EWrapper interface
    that allows more straightforward response processing
    from the IB Gateway or an instance of TWS.
    """

    def init_error(self):
        """
        Place all of the error messages from IB into a
        Python queue, which can be accessed elsewhere.
        """
        error_queue = queue.Queue()
        self._errors = error_queue

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

    def init_time(self):
        """
        Instantiates a new queue to store the server
        time, assigning it to a 'private' instance
        variable and also returning it.

        Returns
        -------
        `Queue`
            The time queue instance.
        """
        time_queue = queue.Queue()
        self._time_queue = time_queue
        return time_queue

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
