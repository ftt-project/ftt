from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult

from ftt.handlers.securities_steps.portfolio_associated_securities import (
    PortfolioAssociatedSecuritiesStep,
)
from ftt.handlers.securities_steps.securities_load_by_symbols_step import (
    SecuritiesLoadBySymbolsStep,
)
from ftt.storage import schemas


class SecuritiesLoadHandler(Handler):
    """
    Handler for loading securities from database.
    """

    params = ("security_symbols",)

    handlers = [
        (SecuritiesLoadBySymbolsStep, "security_symbols"),
        (ReturnResult, SecuritiesLoadBySymbolsStep.key),
    ]


class PortfolioSecuritiesLoadHandler(Handler):
    """
    Loads PortfolioSecurity objects by given Portfolio

    Returns:
    --------
        Result[list[schemas.Security], str]: Result with list of Security
    """

    params = {
        "portfolio": schemas.Portfolio,
    }

    handlers = [
        (PortfolioAssociatedSecuritiesStep, "portfolio"),
        (ReturnResult, PortfolioAssociatedSecuritiesStep.key),
    ]
