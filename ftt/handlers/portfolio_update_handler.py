from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_update_step import PortfolioUpdateStep


class PortfolioUpdateHandler(Handler):
    params = (
        "portfolio",
        "params",
    )

    handlers = [
        (PortfolioUpdateStep, "portfolio", "params"),
        (ReturnResult, PortfolioUpdateStep.key),
    ]
