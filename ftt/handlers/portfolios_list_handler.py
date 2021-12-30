from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolios_list_step import PortfoliosListStep


class PortfoliosListHandler(Handler):
    params = ()

    handlers = [(PortfoliosListStep,), (ReturnResult, PortfoliosListStep.key)]
