from typing import Optional

from nubia import argument, command, context

from trade.cli.renderers.weights.weights_list import WeightsList
from trade.handlers.portfolio_load_handler import PortfolioLoadHandler
from trade.handlers.portfolio_version_activation_handler import PortfolioVersionActivationHandler
from trade.handlers.portfolio_version_loading_handler import PortfolioVersionLoadHandler
from trade.handlers.weights_calculation_handler import WeightsCalculationHandler
from trade.handlers.weights_list_handler import WeightsListHandler


@command("portfolio-versions")
class PortfolioVersionsCommands:
    """
    Portfolio Versions managing
    """

    def __init__(self, portfolio_id: Optional[int] = None):
        ctx = context.get_context()
        self.portfolio_in_use = int(portfolio_id or ctx.portfolio_in_use)

    @command
    @argument(
        "portfolio_version_id", description="Portfolio Version ID", positional=True
    )
    @argument("period_start", description="Beginning of period of historical prices")
    @argument("period_end", description="Ending of period of historical prices")
    @argument(
        "interval",
        description="Trading interval",
        choices=["1m", "5m", "15m", "1d", "1wk", "1mo"],
    )
    def balance(
            self,
            portfolio_version_id: int,
            period_start: str = None,
            period_end: str = None,
            interval: str = None,
    ) -> None:
        """
        Balance portfolio version

        `save` False is not yet implemented
        """
        ctx = context.get_context()

        if self.portfolio_in_use is None:
            ctx.console.print(
                "[yellow]Select portfolio using `portfolio use ID` command"
            )
            return

        portfolio_result = PortfolioLoadHandler().handle(
            portfolio_id=self.portfolio_in_use
        )
        if portfolio_result.is_err():
            ctx.console.print(f"[red]{portfolio_result.err().value}")
            return

        period_start = (
            period_start
            if period_start is not None
            else portfolio_result.value.period_start
        )
        period_end = (
            period_end if period_end is not None else portfolio_result.value.period_end
        )
        interval = interval if interval is not None else portfolio_result.value.interval

        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )
        if portfolio_version_result.is_err():
            ctx.console.print(f"[red]{portfolio_version_result.err().value}")
            return

        weights_result = WeightsCalculationHandler().handle(
            portfolio=portfolio_result.value,
            portfolio_version=portfolio_version_result.value,
            start_period=period_start,
            end_period=period_end,
            interval=interval,
            persist=True,
        )

        if weights_result.is_err():
            ctx.console.print(
                "[red]:disappointed: Failed to calculate weights for this portfolio:"
            )
            ctx.console.print(f"    [red]:right_arrow: {weights_result.err().value}")
            return

        result = WeightsListHandler().handle(
            portfolio_version=portfolio_version_result.value
        )
        WeightsList(
            ctx,
            result.value,
            f"Portfolio Version [bold cyan]#{portfolio_version_result.value.id}[/bold cyan] list of weights",
        ).render()

    @command
    @argument(
        "portfolio_version_id", description="Portfolio Version ID", positional=True
    )
    def activate(self, portfolio_version_id):
        """
        Activate the indicated version of portfolio
        """
        ctx = context.get_context()
        #
        # PortfolioVersionActivationHandler().handle(
        #     portfolio_version_id=portfolio_version_id,
        #     portfolio=portfolio
        # )

    @command
    @argument(
        "portfolio_version_id", description="Portfolio Version ID", positional=True
    )
    def deactivate(self, portfolio_version_id):
        pass

    def statistic(self):
        """
        Distribution of weighs/$
        """
        pass
