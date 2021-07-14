from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolios_list_step import PortfoliosListStep


class PortfoliosListHandler(Handler):
    handlers = [(PortfoliosListStep,), ReturnResult(PortfoliosListStep.key)]
