from trade.handlers.handler import Handler
from trade.handlers.map_steps import MapSteps
from trade.handlers.portfolio_create_step import PortfolioCreateStep
from trade.handlers.portfolio_version_create_step import PortfolioVersionCreateStep


class PortfolioCreationHandler(Handler):
    handlers = [
        PortfolioCreateStep,
        MapSteps(
            (PortfolioVersionCreateStep.key, "portfolio",),
            (PortfolioCreateStep.key, "result",)
        ),
        PortfolioVersionCreateStep,
    ]
