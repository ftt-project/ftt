import os
from unittest.mock import call

import pytest

import ftt
from ftt.cli.commands.portfolios_commands import PortfoliosCommands
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
from ftt.storage.models import Portfolio


class TestPortfoliosCommands:
    @pytest.fixture
    def subject(self):
        return PortfoliosCommands()

    @pytest.fixture(autouse=True)
    def mock_context(self, mocker, context):
        mocker.patch("ftt.cli.commands.portfolios_commands.context", new=context)

    def absolute_path(self, file):
        path = os.path.dirname(ftt.__file__)
        path = os.path.join(path, "..", "config", file)
        return os.path.abspath(path)

    @pytest.fixture
    def path_to_config(self):
        return self.absolute_path("example_portfolio.yml")

    def test_list(self, subject, mocker, portfolio):
        mocked = mocker.patch("ftt.cli.commands.portfolios_commands.PortfoliosList")
        subject.list()

        assert type(mocked.call_args[0][1]) == list
        assert portfolio in mocked.call_args[0][1]

    def test_details_renders_portfolio_details(
        self, subject, mocker, portfolio, portfolio_version
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioDetails",
            **{"return_value.render.return_value": True}
        )
        subject.details(portfolio.id)

        assert portfolio == mocked.call_args[0][1]

    def test_details_renders_portfolio_versions_list(
        self, subject, mocker, portfolio, portfolio_version
    ):
        mocked = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioVersionsList",
            **{"return_value.render.return_value": True}
        )
        subject.details(portfolio.id)

        assert portfolio_version in mocked.call_args[0][1]

    def test_details_writes_message_when_portfolio_not_found(self, subject, context):
        subject.details(101)

        context.get_context.return_value.console.print.assert_has_calls(
            [call("Portfolio with ID 101 does not exist", style="red")]
        )

    def test_import_correct_config_from_file(
        self,
        subject,
        path_to_config,
        mock_external_info_requests,
        mock_external_historic_data_requests,
    ):
        before = Portfolio.select().count()
        subject.import_from_file(path_to_config)
        after = Portfolio.select().count()

        assert (after - before) == 1

    def test_writes_message_on_config_parsing_failure(
        self,
        subject,
        mocker,
        path_to_config,
        context,
        mock_external_info_requests,
        mock_external_historic_data_requests,
    ):
        mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioConfigHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        portfolio_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioCreationHandler",
        )
        subject.import_from_file(path_to_config)
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[bold red]Failed to read config file:")]
        )

        portfolio_mocker.assert_not_called()

    def test_writes_message_on_portfolio_creation_failure(
        self, subject, mocker, path_to_config, context
    ):
        mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioCreationHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        securities_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.SecuritiesInformationPricesLoadingHandler",
        )
        subject.import_from_file(path_to_config)

        securities_mocker.assert_not_called()
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Failed to create portfolio:")]
        )

    def test_on_correct_config_request_assets_info(
        self, subject, mocker, path_to_config
    ):
        securities_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.SecuritiesInformationPricesLoadingHandler",
            **{"return_value.handle.return_value.value": True}
        )
        association_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioAssociateSecuritiesHandler",
            **{"return_value.handle.return_value.value": True}
        )
        subject.import_from_file(path_to_config)

        securities_mocker.return_value.handle.assert_called_once()
        association_mocker.return_value.handle.assert_called_once()

    def test_writes_message_on_securities_loading_failure(
        self, subject, mocker, path_to_config, context
    ):
        mocker.patch(
            "ftt.cli.commands.portfolios_commands.SecuritiesInformationPricesLoadingHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        association_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioAssociateSecuritiesHandler",
        )

        subject.import_from_file(path_to_config)

        association_mocker.assert_not_called()
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Failed to load securities information:")]
        )

    def test_update_call_update_handler(self, subject, portfolio, mocker):
        update_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioUpdateHandler",
            **{"return_value.handle.return_value.value": True}
        )
        prompt_mocker = mocker.patch("ftt.cli.commands.portfolios_commands.prompt")

        subject.update(portfolio_id=portfolio.id)

        prompt_mocker.assert_called_once_with("New name: ", default=portfolio.name)
        update_mocker.return_value.handle.assert_called_once()

    def test_update_writes_message_on_update(self, subject, portfolio, mocker, context):
        prompt_mocker = mocker.patch("ftt.cli.commands.portfolios_commands.prompt")

        subject.update(portfolio_id=portfolio.id)

        prompt_mocker.assert_called_once_with("New name: ", default=portfolio.name)
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[green]Portfolio successfully updated")]
        )

    def test_update_writes_message_on_update_failure(
        self, subject, portfolio, mocker, context
    ):
        prompt_mocker = mocker.patch("ftt.cli.commands.portfolios_commands.prompt")
        update_mock = mocker.patch(
            "ftt.cli.commands.portfolios_commands.PortfolioUpdateHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        update_mock.return_value.handle.return_value.is_ok.return_value = False
        update_mock.return_value.handle.return_value.value = "error"

        subject.update(portfolio_id=portfolio.id)

        prompt_mocker.assert_called_once_with("New name: ", default=portfolio.name)
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Failed to update portfolio:"), call("error")]
        )

    def test_create_portfolio(self, subject, mocker, context):
        prompt_mocker = mocker.patch(
            "ftt.cli.commands.portfolios_commands.CreatePortfolioPromptsHandler"
        )
        prompt_mocker.return_value.handle.return_value.is_err.return_value = False
        prompt_mocker.return_value.handle.return_value.value = {
            "portfolio_dto": PortfolioDTO(name="Utilities"),
            "portfolio_version_dto": PortfolioVersionDTO(
                value=113.0,
                period_start="2019-01-01",
                period_end="2019-12-31",
                interval="1d",
            ),
        }

        subject.create()

        context.get_context.return_value.console.print.assert_any_call(
            "[green]Portfolio successfully created"
        )
