from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_update_step import PortfolioUpdateStep


class PortfolioUpdateHandler(Handler):
    params = (
        "portfolio",
        "dto",
    )

    handlers = [
        (PortfolioUpdateStep, "portfolio", "dto"),
        (ReturnResult, PortfolioUpdateStep.key),
    ]
