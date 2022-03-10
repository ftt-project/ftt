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

    def obtain_server_time(self):
        return self._implementation.obtain_server_time()
