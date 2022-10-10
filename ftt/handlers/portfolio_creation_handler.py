from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep


class PortfolioCreationHandler(Handler):
    params = ("name",)

    handlers = [
        (PortfolioCreateStep, "name"),
        (ReturnResult, PortfolioCreateStep.key),
    ]
