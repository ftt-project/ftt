from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from ftt.handlers.securities_steps.securities_associate_with_portfolio_step import SecuritiesAssociateWithPortfolioStep
from ftt.storage import schemas


class PortfolioCreationHandler(Handler):
    params = {
        "portfolio": schemas.Portfolio,
        "securities": list[schemas.Security],
    }

    handlers = [
        (PortfolioCreateStep, "portfolio"),
        (SecuritiesAssociateWithPortfolioStep, PortfolioCreateStep.key, "securities"),
        (ReturnResult, PortfolioCreateStep.key),
    ]
