from nubia import argument, command, context  # type: ignore
from prompt_toolkit import prompt

from ftt.cli.handlers.create_portfolio_prompts_handler import (
    CreatePortfolioPromptsHandler,
)
from ftt.cli.renderers import PortfoliosList
from ftt.cli.renderers.portfolio_versions.portfolio_version_details import (
    PortfolioVersionBriefDetails,
)
from ftt.cli.renderers.portfolio_versions.portfolio_versions_list import (
    PortfolioVersionsList,
)
from ftt.cli.renderers.portfolios.portfolio_details import PortfolioDetails
from ftt.cli.renderers.weights.weights_list import WeightsList
from ftt.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from ftt.handlers.portfolio_config_handler import PortfolioConfigHandler
from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_update_handler import PortfolioUpdateHandler
from ftt.handlers.portfolio_version_load_active_handler import (
    PortfolioVersionLoadActiveHandler,
)
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.handlers.securities_information_prices_loading_handler import (
    SecuritiesInformationPricesLoadingHandler,
)
from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO
from ftt.storage.data_objects.security_dto import SecurityDTO


@command("portfolios")
class PortfoliosCommands:
    """
    Portfolio managing commands
    """

    def __init__(self):
        self.context = context.get_context()

    @command
    def list(self) -> None:
        """
        List existing portfolios
        """
        ctx = context.get_context()
        result = PortfoliosListHandler().handle()
        PortfoliosList(ctx, result.value).render()

    @command
    @argument("portfolio_id", description="Portfolio ID", positional=True, type=int)
    def details(self, portfolio_id: int) -> None:
        """
        Display details of portfolio by its ID
        """
        ctx = context.get_context()

        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        if portfolio_result.is_err():
            ctx.console.print(portfolio_result.unwrap_err(), style="red")
            return
        PortfolioDetails(ctx, portfolio_result.value).render()

        versions_result = PortfolioVersionsListHandler().handle(
            portfolio=portfolio_result.value
        )
        PortfolioVersionsList(ctx, versions_result.value).render()

        active_portfolio_version_result = PortfolioVersionLoadActiveHandler().handle(
            portfolio_id=portfolio_result.value.id
        )

        if active_portfolio_version_result.is_err():
            ctx.console.print(
                f"Failed to load active portfolio version for portfolio #{portfolio_result.value.id}",
                style="red",
            )
            return

        if active_portfolio_version_result.value:
            PortfolioVersionBriefDetails(
                ctx, active_portfolio_version_result.value
            ).render()

            result = WeightsListHandler().handle(
                portfolio_version=active_portfolio_version_result.value
            )

            WeightsList(
                ctx,
                result.value,
                f"Active Portfolio Version [bold cyan]#{active_portfolio_version_result.value.id}[/bold cyan] "
                f"list of weights",
            ).render()
        else:
            ctx.console.print(
                f"\nPortfolio #{portfolio_result.value.id} do not have any active portfolio version."
            )
            ctx.console.print(
                f"Use `portfolio-versions securities-list portfolio-version-id={versions_result.value[-1]}` "
                f"to display weights of particular version."
            )

    @command("import")
    @argument("path", description="YAML file to import", positional=True)
    def import_from_file(self, path: str) -> None:
        """
        Import from yml file
        """
        # TODO refactor this method
        ctx = context.get_context()
        config_result = PortfolioConfigHandler().handle()
        if config_result.is_err():
            ctx.console.print("[bold red]Failed to read config file:")
            ctx.console.print(config_result.value)
            return

        portfolio_result = PortfolioCreationHandler().handle(
            name=config_result.value.name,
            value=config_result.value.budget,
            period_start=config_result.value.period_start,
            period_end=config_result.value.period_end,
            interval=config_result.value.interval,
        )
        if portfolio_result.is_ok():
            ctx.console.print("[green]Portfolio successfully created")
        else:
            ctx.console.print("[red]Failed to create portfolio:")
            ctx.console.print(portfolio_result.value)
            return

        with ctx.console.status("[green]Loading securities information") as _:
            for symbol in config_result.value.symbols:
                ctx.console.print(f"- {symbol}")

            # TODO why both?
            securities_result = SecuritiesInformationPricesLoadingHandler().handle(
                securities=[
                    SecurityDTO(symbol=symbol) for symbol in config_result.value.symbols
                ],
                portfolio_version=portfolio_result.value.versions[0],
            )
            if securities_result.is_ok():
                ctx.console.print("[green]Securities information successfully imported")
            else:
                ctx.console.print("[red]Failed to load securities information:")
                ctx.console.print(securities_result.value)
                return

        association_result = PortfolioAssociateSecuritiesHandler().handle(
            securities=[
                SecurityDTO(symbol=symbol) for symbol in config_result.value.symbols
            ],
            portfolio_version=portfolio_result.value.versions[0],
        )
        if association_result.is_ok():
            ctx.console.print(
                "[green]Securities successfully associated with portfolio"
            )
        else:
            ctx.console.print("[red]Failed to associate securities with portfolio:")
            ctx.console.print(association_result.value)

    @command("update")
    @argument("portfolio_id", description="Portfolio ID", positional=True, type=int)
    def update(self, portfolio_id: int) -> None:
        """
        Update portfolio by ID
        Possible to update attributes:
            - name
        """
        ctx = context.get_context()

        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        if portfolio_result.is_err():
            ctx.console.print(f"[red]{portfolio_result.err().value}")
            return

        params = {}
        new_name = prompt("New name: ", default=portfolio_result.value.name)

        if new_name != portfolio_result.value.name:
            params["name"] = new_name

        if len(params) == 0:
            ctx.console.print("[green]Nothing to update")
            return

        dto = PortfolioDTO(**params)
        result = PortfolioUpdateHandler().handle(
            portfolio=portfolio_result.value, dto=dto
        )
        if result.is_ok():
            ctx.console.print("[green]Portfolio successfully updated")
        else:
            ctx.console.print("[red]Failed to update portfolio:")
            ctx.console.print(result.value)

    @command("create")
    def create(self) -> None:
        """
        Create a new portfolio
        """
        prompt_result = CreatePortfolioPromptsHandler().handle()

        if prompt_result.is_err():
            self.context.console.print("[red]Correct your input to proceed")
            self.context.console.print(prompt_result.value)
            return

        portfolio_dto = prompt_result.value["portfolio_dto"]
        portfolio_version_dto = prompt_result.value["portfolio_version_dto"]
        # TODO: refactor to use dto in handler
        result = PortfolioCreationHandler().handle(
            name=portfolio_dto.name,
            value=portfolio_version_dto.value,
            period_start=portfolio_version_dto.period_start,
            period_end=portfolio_version_dto.period_end,
            interval=portfolio_version_dto.interval,
        )

        if result.is_ok():
            self.context.console.print("[green]Portfolio successfully created")
        else:
            self.context.console.print("[red]Failed to create portfolio:")
            self.context.console.print(f"  {result.value.value}")
