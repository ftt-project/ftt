from unittest.mock import call

from ftt.cli.commands import backtrade_commands


def test_run_backtrade(portfolio_version, mocker, context):
    mocked = mocker.patch(
        "ftt.cli.commands.backtrade_commands.BacktradeHandler",
        **{
            "return_value.handle.return_value.is_err.return_value": False,
            "return_value.handle.return_value.value": "Result",
        }
    )

    context = mocker.patch(
        "ftt.cli.commands.backtrade_commands.context",
    )
    print_mock = context.get_context.return_value.console.print

    backtrade_commands.backtrade(portfolio_version_id=1)

    mocked.return_value.handle.assert_called_once()
    print_mock.assert_any_call("Backtrading result: Result")
