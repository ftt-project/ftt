from nubia import command, context  # type: ignore

from ftt.cli.renderers.portfolios.portfolio_details import PortfolioDetails
from ftt.cli.renderers.weights.weights_list import WeightsList
from ftt.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from ftt.handlers.portfolio_config_handler import PortfolioConfigHandler
from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.handlers.portfolio_optimization_handler import PortfolioOptimizationHandler
from ftt.handlers.portfolio_stats_handler import PortfoliosStatsHandler
from ftt.handlers.securities_information_prices_loading_handler import (
    SecuritiesInformationPricesLoadingHandler,
)
from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.portfolio_management.allocation_strategies import AllocationStrategyResolver
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
)
from ftt.storage.data_objects.security_dto import SecurityDTO


@command
def example():
    """
    Create example portfolio with weights from example config
    """
    ctx = context.get_context()

    config_result = PortfolioConfigHandler().handle()
    if config_result.is_err():
        ctx.console.print("Failed to load example config file.", style="red")
        ctx.console.print(config_result.unwrap_err())
        return

    result = PortfolioCreationHandler().handle(
        name=config_result.value.name,
        value=config_result.value.budget,
        period_start=config_result.value.period_start,
        period_end=config_result.value.period_end,
        interval=config_result.value.interval,
    )
    portfolio = result.value

    ctx.console.print("Portfolio successfully created", style="bold green")
    PortfolioDetails(ctx, portfolio).render()

    security_dtos = [
        SecurityDTO(symbol=symbol) for symbol in config_result.value.symbols
    ]

    with ctx.console.status("[bold green]Loading securities information") as _:
        for symbol in config_result.value.symbols:
            ctx.console.print(f"- {symbol}")

        result = SecuritiesInformationPricesLoadingHandler().handle(
            portfolio_version=portfolio.versions[0],
            securities=security_dtos,
        )
        _ = result.value

    with ctx.console.status(
        "[bold green]Portfolio successfully associated with securities"
    ) as _:
        _ = PortfolioAssociateSecuritiesHandler().handle(
            securities=security_dtos, portfolio_version=portfolio.versions[0]
        )

    with ctx.console.status("[bold green]Calculating weights") as _:
        _ = PortfolioOptimizationHandler().handle(
            portfolio_version_id=portfolio.versions[0].id,
            optimization_strategy_name=OptimizationStrategyResolver.strategies()[0],
            allocation_strategy_name=AllocationStrategyResolver.strategies[0],
        )

    result = PortfoliosStatsHandler().handle(portfolio_version=portfolio.versions[0])
    if result.is_ok():
        ctx.console.print("Weights are calculated and saved", style="bold green")
    else:
        ctx.console.print(result.unwrap_err())

    weights_result = WeightsListHandler().handle(
        portfolio_version=portfolio.versions[0]
    )
    WeightsList(ctx, weights_result.value).render()
