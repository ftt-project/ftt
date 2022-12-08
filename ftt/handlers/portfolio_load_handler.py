from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep
from ftt.storage import schemas


class PortfolioLoadHandler(Handler):
    """
    Returns a portfolio schema model with all properties loaded from DB based on the portfolio ID.
    """
    params = {"portfolio": schemas.Portfolio}

    handlers = [
        (PortfolioLoadStep, "portfolio"),
        (ReturnResult, PortfolioLoadStep.key),
    ]
