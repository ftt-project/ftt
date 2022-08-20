from nubia import command, context, argument  # type: ignore

from ftt.handlers.backtrade_handler import BacktradeHandler


@command
@argument("portfolio_version_id", description="Portfolio ID", positional=True, type=int)
def backtrade(portfolio_version_id: int) -> None:
    ctx = context.get_context()
    result = BacktradeHandler().handle(portfolio_version_id=portfolio_version_id)
    if result.is_err():
        ctx.console.print(result.unwrap_err(), style="red")
        return

    ctx.console.print(f"Backtrading result: {result.value}")
