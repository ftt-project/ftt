from unittest.mock import call

import pytest

from ftt.cli.commands.portfolio_versions_commands import PortfolioVersionsCommands
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class TestPortfolioVersionsCommands:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsCommands

    @pytest.fixture(autouse=True)
    def mock_context(self, mocker, context):
        mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.context", new=context
        )

    def test_optimize_portfolio(
        self, subject, portfolio, portfolio_version, security, mocker, context
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.PortfolioOptimizationHandler"
        )
        mocked.return_value.handle.return_value = mocker.Mock(is_okay=True)

        subject().optimize(portfolio_version.id, "historical", "default")

        mocked.return_value.handle.assert_called_once()

    def test_optimize_requires_associated_securities(
        self, subject, portfolio_version, context
    ):
        subject().optimize(
            portfolio_version_id=portfolio_version.id,
            optimization_strategy="historical",
            allocation_strategy="default",
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [
                call(
                    "    [red]:right_arrow: No securities associated with portfolio version 1"
                )
            ]
        )

    def test_optimize_prints_error_when_no_specified_portfolio_version_found(
        self, subject, portfolio, portfolio_version, context
    ):
        subject().optimize(portfolio_version_id=100, optimization_strategy="historical")

        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Portfolio Version with ID 100 does not exist")]
        )

    def test_optimize_period_and_interval_arguments_are_optional(
        self, subject, portfolio, portfolio_version, mocker
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.PortfolioOptimizationHandler"
        )
        mocked.return_value.handle.return_value = mocker.Mock(is_okay=True)

        subject().optimize(
            portfolio_version_id=portfolio_version.id,
            optimization_strategy="historical",
        )
        mocked.return_value.handle.assert_called_once()

    def test_activate(self, subject, portfolio, portfolio_version, weight, context):
        portfolio_version.active = False
        portfolio_version.save()
        subject().activate(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]Portfolio version {portfolio_version.id} set active")]
        )

    def test_activate_active_portfolio_version(
        self, subject, portfolio, portfolio_version, context
    ):
        portfolio_version.active = True
        portfolio_version.save()
        subject().activate(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Failed to activate portfolio version #{portfolio_version.id}"
        )
        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Portfolio version #{portfolio_version.id} is already active"
        )

    def test_activate_errors_when_no_weights_associated(
        self, subject, portfolio, portfolio_version, context
    ):
        subject().activate(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Failed to activate portfolio version #{portfolio_version.id}"
        )
        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Portfolio version #{portfolio_version.id} does not have any weights associated. Run balance step first."
        )

    def test_deactivate(self, subject, portfolio, portfolio_version, context):
        portfolio_version.active = True
        portfolio_version.save()
        subject().deactivate(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]Portfolio Version {portfolio_version.id} is deactivated")]
        )

    def test_deactivate_not_active_portfolio(
        self, subject, portfolio, portfolio_version, context
    ):
        portfolio_version.active = False
        portfolio_version.save()
        subject().deactivate(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Failed to deactivate portfolio version #{portfolio_version.id}"
        )
        context.get_context.return_value.console.print.assert_any_call(
            f"[yellow]Portfolio version #{portfolio_version.id} is not active"
        )

    def test_update_active_portfolio_version(
        self, subject, portfolio, portfolio_version, context
    ):
        portfolio_version.active = True
        portfolio_version.save()
        subject().update(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_has_calls(
            [
                call(
                    f"[yellow]Portfolio Version #{portfolio_version.id} is active and cannot be updated"
                )
            ]
        )

    def test_update_not_active_portfolio_version(
        self, subject, portfolio, portfolio_version, context, mocker
    ):
        portfolio_version.active = False
        portfolio_version.save()
        prompt_mocker = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.UpdatePortfolioPromptsHandler"
        )
        prompt_mocker.return_value.handle.return_value.value = PortfolioVersionDTO(
            value=100,
            period_start="2021-01-01",
            period_end="2021-04-20",
            interval="1d",
        )

        subject().update(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]Portfolio Version #{portfolio_version.id} is updated")]
        )

    def test_create_from_existing(
        self, subject, portfolio, portfolio_version, context, mocker
    ):
        prompt_mocker = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.prompt"
        )
        prompt_mocker.side_effect = [100, "2021-01-01", "2021-04-20", "1d"]

        subject().create_from_existing(
            portfolio_version_id=portfolio_version.id,
            portfolio_id=portfolio.id,
        )

        prompt_mocker.assert_any_call("Account value: ", default="30000.00")
        prompt_mocker.assert_any_call(
            "Period start: ", default=str(portfolio_version.period_start)
        )
        prompt_mocker.assert_any_call(
            "Period end: ", default=str(portfolio_version.period_end)
        )
        prompt_mocker.assert_any_call("Interval: ", default=portfolio_version.interval)

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]The new Portfolio Version #2 is created")]
        )

    def test_create_new(self, subject, portfolio, context, mocker):
        prompt_mocker = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.prompt"
        )
        prompt_mocker.side_effect = [100, "2021-01-01", "2021-04-20", "1d"]

        handler_mocker = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.PortfolioVersionCreationHandler"
        )
        handler_mocker.return_value.handle.return_value.value.id = 111

        subject().create(portfolio_id=portfolio.id)

        prompt_mocker.assert_any_call("Account value: ")
        prompt_mocker.assert_any_call("Period start: ")
        prompt_mocker.assert_any_call("Period end: ")
        prompt_mocker.assert_any_call("Interval: ")

        handler_mocker.return_value.handle.assert_called_once_with(
            portfolio=portfolio,
            value=100,
            period_start="2021-01-01",
            period_end="2021-04-20",
            interval="1d",
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [call(f"[green]The new Portfolio Version #111 is created")]
        )

    def test_add_securities(
        self,
        subject,
        portfolio,
        portfolio_version,
        context,
        mock_external_info_requests,
        mock_external_historic_data_requests,
    ):
        subject().securities_add(
            portfolio_version_id=portfolio_version.id, securities="MSFT"
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [
                call(
                    f"[green]Securities were added to Portfolio Version #{portfolio_version.id}"
                )
            ]
        )

    def test_remove_securities(
        self,
        subject,
        portfolio,
        portfolio_version,
        context,
        weight,
        security,
    ):
        subject().securities_remove(
            portfolio_version_id=portfolio_version.id, securities=security.symbol
        )

        context.get_context.return_value.console.print.assert_has_calls(
            [
                call(
                    f"[green]Securities were removed from Portfolio Version #{portfolio_version.id}"
                )
            ]
        )

    def test_securities_list_displays_list_of_weights(
        self, subject, portfolio_version, mocker, weight, security
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.WeightsList",
            **{"return_value.render.return_value": True},
        )

        subject().securities_list(portfolio_version_id=portfolio_version.id)

        assert weight in mocked.call_args[0][1]

    def test_securities_list_displays_error_message_when_no_version_found(
        self, subject, context
    ):
        subject().securities_list(portfolio_version_id=111)

        context.get_context.return_value.console.print.assert_any_call(
            "[red]Failed to get portfolio version details:"
        )
        context.get_context.return_value.console.print.assert_any_call(
            "Portfolio Version with ID 111 does not exist"
        )

    def test_details_displays_portfolio_version_details(
        self, subject, portfolio_version, mocker
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.PortfolioVersionDetails",
            **{"return_value.render.return_value": True},
        )

        subject().details(portfolio_version_id=portfolio_version.id)

        assert portfolio_version == mocked.call_args[0][1]

    def test_synchronize_positions_displays_success_message(
        self, subject, context, portfolio_version, mocker, order
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolio_versions_commands.PositionsSynchronizationHandler"
        )
        mocked.return_value.handle.return_value.is_ok.return_value = True
        mocked.return_value.handle.return_value.value = [order]

        subject().synchronize_positions(portfolio_version_id=portfolio_version.id)

        context.get_context.return_value.console.print.assert_any_call(
            f"[green]Positions were synchronized for Portfolio Version #{portfolio_version.id}"
        )
        context.get_context.return_value.console.print.assert_any_call(
            f"[green]Orders were created for Portfolio Version #{portfolio_version.id}: [{order.id}]"
        )
