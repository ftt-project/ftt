from ftt.cli.commands import example_commands


def test_example_create_portfolio_and_version(mocker):
    context = mocker.patch(
        "ftt.cli.commands.example_commands.context",
    )
    print_mock = context.get_context.return_value.console.print
    print_mock.return_value = None

    mocker.patch(
        "ftt.cli.commands.example_commands.PortfolioOptimizationHandler",
        **{"return_value.handle.return_value": None}
    )

    example_commands.example()

    print_mock.assert_any_call("Portfolio successfully created", style="bold green")
    print_mock.assert_any_call("Weights are calculated and saved", style="bold green")
