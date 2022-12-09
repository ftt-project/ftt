from ftt.handlers.handler.context import Context
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_version_create_step import (
    PortfolioVersionCreateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_next_version_calculation_step import (
    PortfolioVersionNextVersionCalculationStep,
)
from ftt.storage import schemas


class PortfolioVersionCreationHandler(Handler):
    params = {"portfolio_version": schemas.PortfolioVersion}

    handlers = [
        (PortfolioVersionNextVersionCalculationStep, "portfolio_version"),
        Context(rename=PortfolioVersionNextVersionCalculationStep.key, to="version"),
        (
            PortfolioVersionCreateStep,
            "portfolio_version",
            "version",
        ),
        (ReturnResult, PortfolioVersionCreateStep.key),
    ]
