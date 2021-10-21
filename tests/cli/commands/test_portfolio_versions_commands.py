from unittest.mock import call

import pytest

from ftt.cli.commands.portfolio_versions_commands import PortfolioVersionsCommands


class TestPortfolioVersionsCommands:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsCommands

    @pytest.fixture(autouse=True)
    def mock_context(self, mocker, context):
        mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.context", new=context
        )

    def test_balance_calculating_weights(
        self, subject, portfolio, portfolio_version, security, mocker, context
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.WeightsCalculationHandler"
        )
        mocked.return_value.handle.return_value = mocker.Mock(is_okay=True)

        context.get_context.return_value.portfolio_in_use = portfolio.id

        subject().balance(portfolio_version.id, "2021-01-01", "2021-04-20", "1d")

        mocked.return_value.handle.assert_called_once()

    def test_accepts_portfolio_id_in_constructor(
        self, subject, portfolio, portfolio_version, security, mocker
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.WeightsCalculationHandler"
        )
        mocked.return_value.handle.return_value = mocker.Mock(is_okay=True)

        subject(portfolio_id=portfolio.id).balance(
            portfolio_version.id, "2021-01-01", "2021-04-20", "1d"
        )

        mocked.return_value.handle.assert_called_once()

    def test_requires_active_portfolio(self, subject, portfolio_version, context):
        subject(portfolio_id=100).balance(
            portfolio_version.id, "2021-01-01", "2021-04-20", "1d"
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Portfolio with ID 100 does not exist")]
        )

    def test_prints_error_when_no_specified_portfolio_version_found(
        self, subject, portfolio, portfolio_version, context
    ):
        subject(portfolio_id=portfolio.id).balance(
            100, "2021-01-01", "2021-04-20", "1d"
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Portfolio Version with ID 100 does not exist")]
        )

    def test_balance_period_and_interval_arguments_are_optional(
        self, subject, portfolio, portfolio_version, mocker
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.WeightsCalculationHandler"
        )
        mocked.return_value.handle.return_value = mocker.Mock(is_okay=True)

        subject(portfolio_id=portfolio.id).balance(
            portfolio_version_id=portfolio_version.id
        )
        mocked.return_value.handle.assert_called_once()

    def test_activate(self, subject, portfolio, portfolio_version, context):
        portfolio_version.active = False
        portfolio_version.save()
        subject(portfolio_id=portfolio.id).activate(
            portfolio_version_id=portfolio_version.id
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]Portfolio Version {portfolio_version.id} set active")]
        )

    def test_activate_active_portfolio_version(
        self, subject, portfolio, portfolio_version, context
    ):
        portfolio_version.active = True
        portfolio_version.save()
        subject(portfolio_id=portfolio.id).activate(
            portfolio_version_id=portfolio_version.id
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [
                call(
                    f"[yellow]Portfolio Version #{portfolio_version.id} is already active"
                )
            ]
        )

    def test_deactivate(self, subject, portfolio, portfolio_version, context):
        portfolio_version.active = True
        portfolio_version.save()
        subject(portfolio_id=portfolio.id).deactivate(
            portfolio_version_id=portfolio_version.id
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]Portfolio Version {portfolio_version.id} is deactivated")]
        )

    def test_deactivate_not_active_portfolio(
        self, subject, portfolio, portfolio_version, context
    ):
        portfolio_version.active = False
        portfolio_version.save()
        subject(portfolio_id=portfolio.id).deactivate(
            portfolio_version_id=portfolio_version.id
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[yellow]Portfolio Version #{portfolio_version.id} is not active")]
        )
