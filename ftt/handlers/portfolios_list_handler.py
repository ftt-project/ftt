from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolios_list_step import PortfoliosListStep


class PortfoliosListHandler(Handler):
    handlers = [(PortfoliosListStep,), (ReturnResult, PortfoliosListStep.key)]
