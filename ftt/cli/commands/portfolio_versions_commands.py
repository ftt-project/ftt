from nubia import argument, command, context  # type: ignore
from prompt_toolkit import prompt

from ftt.cli.handlers.update_portfolio_prompts_handler import (
    UpdatePortfolioPromptsHandler,
)
from ftt.cli.renderers.portfolio_versions.portfolio_version_details import (
    PortfolioVersionDetails,
)
from ftt.cli.renderers.weights.weights_list import WeightsList
from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_optimization_handler import PortfolioOptimizationHandler
from ftt.handlers.portfolio_version_activation_handler import (
    PortfolioVersionActivationHandler,
)
from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.handlers.portfolio_version_deactivation_handler import (
    PortfolioVersionDeactivationHandler,
)
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_version_securities_adding_handler import (
    PortfolioVersionSecuritiesAddingHandler,
)
from ftt.handlers.portfolio_version_securities_disassociate_handler import (
    PortfolioVersionSecuritiesDisassociateHandler,
)
from ftt.handlers.portfolio_version_updation_handler import (
    PortfolioVersionUpdationHandler,
)
from ftt.handlers.positions_synchronization_handler import (
    PositionsSynchronizationHandler,
)
from ftt.handlers.securities_load_handler import SecuritiesLoadHandler
from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.portfolio_management.allocation_strategies import AllocationStrategyResolver
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
)
from ftt.storage.data_objects import is_empty
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
from ftt.storage.data_objects.security_dto import SecurityDTO


@command("portfolio-versions")
class PortfolioVersionsCommands:
    """
    Portfolio Versions managing
    """

    def __init__(self):
        self.context = context.get_context()

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    @argument(
        "optimization_strategy",
        description="Optimization strategy",
        positional=True,
        type=str,
        choices=OptimizationStrategyResolver.strategies(),
    )
    @argument(
        "allocation_strategy",
        description="Allocation strategy",
        type=str,
        choices=AllocationStrategyResolver.strategies,
    )
    def optimize(
        self,
        portfolio_version_id: int,
        optimization_strategy: str,
        allocation_strategy: str = "default",
    ) -> None:
        """
        Optimize portfolio version

        `save` False is not yet implemented
        """
        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )
        if portfolio_version_result.is_err():
            self.context.console.print(f"[red]{portfolio_version_result.unwrap_err()}")
            return

        optimization_result = PortfolioOptimizationHandler().handle(
            portfolio_version_id=portfolio_version_result.value.id,
            optimization_strategy_name=optimization_strategy,
            allocation_strategy_name=allocation_strategy,
        )

        if optimization_result.is_err():
            self.context.console.print(
                "[red]:disappointed: Failed to calculate weights for this portfolio:"
            )
            self.context.console.print(
                f"    [red]:right_arrow: {optimization_result.unwrap_err()}"
            )
            return

        result = WeightsListHandler().handle(
            portfolio_version=portfolio_version_result.value
        )
        WeightsList(
            self.context,
            result.value,
            f"Portfolio Version [bold cyan]#{portfolio_version_result.value.id}[/bold cyan] list of weights",
        ).render()

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def activate(self, portfolio_version_id: int):
        """
        Activate the indicated version of the portfolio and deactivates the rest
        """
        result = PortfolioVersionActivationHandler().handle(
            portfolio_version_id=portfolio_version_id,
        )

        if result.is_ok():
            self.context.console.print(
                f"[green]Portfolio version {portfolio_version_id} set active"
            )
        else:
            self.context.console.print(
                f"[yellow]Failed to activate portfolio version #{portfolio_version_id}"
            )
            self.context.console.print(f"[yellow]{result.unwrap_err()}")

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def deactivate(self, portfolio_version_id: int):
        """
        Deactivate the indicated version of the portfolio
        """
        result = PortfolioVersionDeactivationHandler().handle(
            portfolio_version_id=portfolio_version_id,
        )

        if result.is_ok():
            self.context.console.print(
                f"[green]Portfolio Version {portfolio_version_id} is deactivated"
            )
        else:
            self.context.console.print(
                f"[yellow]Failed to deactivate portfolio version #{portfolio_version_id}"
            )
            self.context.console.print(f"[yellow]{result.unwrap_err()}")

    def statistic(self):
        """
        Distribution of weighs/$
        """
        pass

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def update(self, portfolio_version_id: int):
        """
        Update the indicated version of the portfolio.
        Only not active portfolio versions can be updated.
        Possible to update attributes:
            - account value
            - period start
            - period end
            - interval
        """
        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )

        if portfolio_version_result.value.active:
            self.context.console.print(
                f"[yellow]Portfolio Version #{portfolio_version_result.value.id} is active and cannot be updated"
            )
            return

        prompt_result = UpdatePortfolioPromptsHandler().handle(
            defaults=PortfolioVersionDTO(
                value=portfolio_version_result.value.value,
                period_start=portfolio_version_result.value.period_start,
                period_end=portfolio_version_result.value.period_end,
                interval=portfolio_version_result.value.interval,
            )
        )

        # TODO: This should be part of the handler and we have to check for input errors here such as empty values
        if is_empty(prompt_result.value):
            self.context.console.print("[green]Nothing to update")
            return

        result = PortfolioVersionUpdationHandler().handle(
            portfolio_version=portfolio_version_result.value, dto=prompt_result.value
        )
        if result.is_ok():
            self.context.console.print(
                f"[green]Portfolio Version #{portfolio_version_result.value.id} is updated"
            )
        else:
            self.context.console.print("[red]Failed to update portfolio:")
            self.context.console.print(result.value)

    @command("create-new")
    @argument(
        "portfolio_id",
        description="Portfolio ID",
        positional=True,
        type=int,
    )
    def create(self, portfolio_id):
        """
        Create a new portfolio version
        """
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)

        # TODO: refactor to use the same logic as the update command
        params = {}
        new_account_value = prompt("Account value: ")
        params["value"] = new_account_value

        new_period_start = prompt("Period start: ")
        params["period_start"] = new_period_start

        new_period_end = prompt("Period end: ")
        params["period_end"] = new_period_end

        new_interval = prompt("Interval: ")
        params["interval"] = new_interval

        result = PortfolioVersionCreationHandler().handle(
            portfolio=portfolio_result.value,
            value=params.get("value"),
            period_start=params.get("period_start"),
            period_end=params.get("period_end"),
            interval=params.get("interval"),
        )
        if result.is_ok():
            self.context.console.print(
                f"[green]The new Portfolio Version #{result.value.id} is created"
            )
        else:
            self.context.console.print("[red]Failed to create portfolio version:")
            self.context.console.print(result.value)

    @command
    @argument(
        "portfolio_id",
        description="Portfolio ID",
        positional=True,
        type=int,
    )
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def create_from_existing(self, portfolio_id: int, portfolio_version_id: int):
        """
        Create a new portfolio version from an existing one
        """
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)

        if portfolio_result.is_err():
            self.context.console.print(portfolio_result.value)
            return

        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )

        if portfolio_version_result.is_err():
            self.context.console.print(portfolio_version_result.value)
            return

        params = {
            "value": portfolio_version_result.value.value,
            "period_start": portfolio_version_result.value.period_start,
            "period_end": portfolio_version_result.value.period_end,
            "interval": portfolio_version_result.value.interval,
        }
        new_account_value = prompt(
            "Account value: ", default=f"{portfolio_version_result.value.value:.2f}"
        )
        if new_account_value != portfolio_version_result.value.value:
            params["value"] = new_account_value

        new_period_start = prompt(
            "Period start: ", default=str(portfolio_version_result.value.period_start)
        )
        if new_period_start != portfolio_version_result.value.period_start:
            params["period_start"] = new_period_start

        new_period_end = prompt(
            "Period end: ", default=str(portfolio_version_result.value.period_end)
        )
        if new_period_end != portfolio_version_result.value.period_end:
            params["period_end"] = new_period_end

        new_interval = prompt(
            "Interval: ", default=portfolio_version_result.value.interval
        )
        if new_interval != portfolio_version_result.value.interval:
            params["interval"] = new_interval

        result = PortfolioVersionCreationHandler().handle(
            portfolio=portfolio_result.value,
            value=params.get("value"),
            period_start=params.get("period_start"),
            period_end=params.get("period_end"),
            interval=params.get("interval"),
        )
        if result.is_ok():
            self.context.console.print(
                f"[green]The new Portfolio Version #{result.value.id} is created"
            )
        else:
            self.context.console.print("[red]Failed to create portfolio version:")
            self.context.console.print(result.value)

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    @argument("securities", description="List of securities separated by space")
    def securities_add(self, portfolio_version_id: int, securities: str):
        """
        Provide list of securities to be added to the indicated portfolio version
        """
        securities_dto = [
            SecurityDTO(symbol=security) for security in securities.split(" ")
        ]

        with self.context.console.status("[green]Loading securities information") as _:
            result = PortfolioVersionSecuritiesAddingHandler().handle(
                portfolio_version_id=portfolio_version_id,
                securities=securities_dto,
            )

        if result.is_ok():
            self.context.console.print(
                f"[green]Securities were added to Portfolio Version #{result.value['portfolio_version'].id}"
            )
        else:
            self.context.console.print(
                "[red]Failed to add security to portfolio version:"
            )
            self.context.console.print(result.value)

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    @argument("securities", description="List of securities separated by space")
    def securities_remove(self, portfolio_version_id: int, securities: str):
        """
        Provide list of securities to be removed from indicated portfolio version
        """

        securities_result = SecuritiesLoadHandler().handle(
            security_symbols=[securities.split(" ")]
        )

        if securities_result.is_err():
            self.context.console.print(securities_result.value)
            return

        result = PortfolioVersionSecuritiesDisassociateHandler().handle(
            portfolio_version_id=portfolio_version_id,
            securities=securities_result.value,
        )

        if result.is_ok():
            self.context.console.print(
                f"[green]Securities were removed from Portfolio Version #{result.value['portfolio_version'].id}"
            )
        else:
            self.context.console.print(
                "[red]Failed to remove security from portfolio version:"
            )
            self.context.console.print(result.value)

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def securities_list(self, portfolio_version_id: int):
        """
        Provide list of securities associated with portfolio version
        """
        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )

        if portfolio_version_result.is_err():
            self.context.console.print("[red]Failed to get portfolio version details:")
            self.context.console.print(portfolio_version_result.unwrap_err())
            return

        weights_result = WeightsListHandler().handle(
            portfolio_version=portfolio_version_result.value
        )

        WeightsList(
            self.context,
            weights_result.value,
            f"Portfolio Version [bold cyan]#{portfolio_version_result.value.id}[/bold cyan] list of weights",
        ).render()

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def details(self, portfolio_version_id: int):
        """
        Provide details of portfolio version
        """
        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )

        if portfolio_version_result.is_err():
            self.context.console.print("[red]Failed to get portfolio version details:")
            self.context.console.print(portfolio_version_result.err().value)
            return

        PortfolioVersionDetails(
            self.context,
            portfolio_version_result.value,
        ).render()

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def synchronize_positions(self, portfolio_version_id: int):
        """
        Synchronize planned and open positions between local and broker systems
        """
        result = PositionsSynchronizationHandler().handle(
            portfolio_version_id=portfolio_version_id
        )

        if result.is_ok():
            self.context.console.print(
                f"[green]Positions were synchronized for Portfolio Version #{portfolio_version_id}"
            )
            self.context.console.print(
                f"[green]Orders were created for Portfolio Version #{portfolio_version_id}: "
                f"{[order.id for order in result.value]}"
            )
        else:
            self.context.console.print("[red]Failed to synchronize positions:")
            self.context.console.print(result.value)
