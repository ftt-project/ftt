from typing import Optional

from nubia import argument, command, context  # type: ignore
from prompt_toolkit import prompt

from ftt.cli.handlers.update_portfolio_prompts_handler import (
    UpdatePortfolioPromptsHandler,
)
from ftt.cli.renderers.weights.weights_list import WeightsList
from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_version_activation_handler import (
    PortfolioVersionActivationHandler,
)
from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.handlers.portfolio_version_deactivation_handler import (
    PortfolioVersionDeactivationHandler,
)
from ftt.handlers.portfolio_version_loading_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_version_securities_adding_handler import (
    PortfolioVersionSecuritiesAddingHandler,
)
from ftt.handlers.portfolio_version_securities_disassociate_handler import (
    PortfolioVersionSecuritiesDisassociateHandler,
)
from ftt.handlers.portfolio_version_updation_handler import (
    PortfolioVersionUpdationHandler,
)
from ftt.handlers.securities_load_handler import SecuritiesLoadHandler
from ftt.handlers.weights_calculation_handler import WeightsCalculationHandler
from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.storage.data_objects import is_empty
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
from ftt.storage.data_objects.security_dto import SecurityDTO


@command("portfolio-versions")
class PortfolioVersionsCommands:
    """
    Portfolio Versions managing
    """

    def __init__(self, portfolio_id: Optional[int] = None):
        self.context = context.get_context()
        self.portfolio_in_use = int(portfolio_id or self.context.portfolio_in_use)

    @command
    @argument(
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def balance(
        self,
        portfolio_version_id: int,
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

        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )
        if portfolio_version_result.is_err():
            ctx.console.print(f"[red]{portfolio_version_result.err().value}")
            return

        weights_result = WeightsCalculationHandler().handle(
            portfolio=portfolio_result.value,
            portfolio_version=portfolio_version_result.value,
            start_period=portfolio_version_result.value.period_start,
            end_period=portfolio_version_result.value.period_end,
            interval=portfolio_version_result.value.interval,
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
        "portfolio_version_id",
        description="Portfolio Version ID",
        positional=True,
        type=int,
    )
    def activate(self, portfolio_version_id: int):
        """
        Activate the indicated version of the portfolio and deactivates the rest
        """
        ctx = context.get_context()

        # TODO handle if not found situation

        result = PortfolioVersionActivationHandler().handle(
            portfolio_version_id=portfolio_version_id,
        )

        if result.is_ok():
            ctx.console.print(
                f"[green]Portfolio version {portfolio_version_id} set active"
            )
        else:
            ctx.console.print(
                f"[yellow]Failed to activate portfolio version #{portfolio_version_id}"
            )
            ctx.console.print(f"[yellow]{result.value.value}")

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
        ctx = context.get_context()

        # TODO refactor, duplicated in `balance` method
        if self.portfolio_in_use is None:
            ctx.console.print(
                "[yellow]Select portfolio using `portfolio use ID` command"
            )
            return

        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )
        portfolio_result = PortfolioLoadHandler().handle(
            portfolio_id=self.portfolio_in_use
        )

        # TODO handle if not found situation

        result = PortfolioVersionDeactivationHandler().handle(
            portfolio_version=portfolio_version_result.value,
            portfolio=portfolio_result.value,
        )

        if result.is_ok():
            ctx.console.print(
                f"[green]Portfolio Version {portfolio_version_id} is deactivated"
            )
        else:
            ctx.console.print(f"[yellow]{result.value.value}")

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
    def create(self):
        """
        Create a new portfolio version
        """
        # TODO refactor, duplicated in `balance` method
        if self.portfolio_in_use is None:
            self.context.console.print(
                "[yellow]Select portfolio using `portfolio use ID` command"
            )
            return
        portfolio_result = PortfolioLoadHandler().handle(
            portfolio_id=self.portfolio_in_use
        )

        params = {}
        new_account_value = prompt("Account value: ")
        params["amount"] = new_account_value

        new_period_start = prompt("Period start: ")
        params["period_start"] = new_period_start

        new_period_end = prompt("Period end: ")
        params["period_end"] = new_period_end

        new_interval = prompt("Interval: ")
        params["interval"] = new_interval

        result = PortfolioVersionCreationHandler().handle(
            portfolio=portfolio_result.value,
            amount=params.get("amount"),
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
    def create_from_existing(self, portfolio_version_id: int):
        """
        Create a new portfolio version from an existing one
        """
        # TODO refactor, duplicated in `balance` method
        if self.portfolio_in_use is None:
            self.context.console.print(
                "[yellow]Select portfolio using `portfolio use ID` command"
            )
            return
        portfolio_result = PortfolioLoadHandler().handle(
            portfolio_id=self.portfolio_in_use
        )

        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=portfolio_version_id
        )
        # TODO handle if not found situation

        params = {}
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
