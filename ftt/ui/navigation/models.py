from ftt.handlers.portfolios_list_handler import PortfoliosListHandler


class PortfoliosModel:
    def __init__(self):
        self._portfolios = None

    @property
    def portfolios(self):
        if self._portfolios is None:
            self._portfolios = PortfoliosListHandler().handle()

        return self._portfolios
