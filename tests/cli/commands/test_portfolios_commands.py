import os
import pathlib
from unittest.mock import call

import pytest

from trade.cli.commands.portfolios_commands import PortfoliosCommands
from trade.storage.models import Portfolio


class TestPortfoliosCommands:
    @pytest.fixture
    def subject(self):
        return PortfoliosCommands()

    @pytest.fixture(autouse=True)
    def mock_context(self, mocker, context):
        mocker.patch("trade.cli.commands.portfolios_commands.context", new=context)

    @pytest.fixture
    def path_to_config(self):
        realpath = pathlib.Path().resolve()
        path = os.path.join(realpath, "config", "example_portfolio.yml")
        return path

    def test_list(self, subject, mocker, portfolio):
        mocked = mocker.patch("trade.cli.commands.portfolios_commands.PortfoliosList")
        mocked.return_value.render.return_value
        subject.list()

        assert type(mocked.call_args[0][1]) == list
        assert portfolio in mocked.call_args[0][1]

    def test_details_renders_portfolio_details(
            self, subject, mocker, portfolio, portfolio_version
    ):
        mocked = mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioDetails",
            **{"return_value.render.return_value": True}
        )
        subject.details(portfolio.id)

        assert portfolio == mocked.call_args[0][1]

    def test_details_renders_portfolio_versions_list(
            self, subject, mocker, portfolio, portfolio_version
    ):
        mocked = mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioVersionsList",
            **{"return_value.render.return_value": True}
        )
        subject.details(portfolio.id)

        assert portfolio_version in mocked.call_args[0][1]

    def test_import_correct_config_from_file(self, subject, path_to_config):
        before = Portfolio.select().count()
        subject.import_from_file(path_to_config)
        after = Portfolio.select().count()

        assert (after - before) == 1

    def test_writes_message_on_config_parsing_failure(
            self, subject, mocker, path_to_config, context
    ):
        mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioConfigHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        portfolio_mocker = mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioCreationHandler",
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
            "trade.cli.commands.portfolios_commands.PortfolioCreationHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        securities_mocker = mocker.patch(
            "trade.cli.commands.portfolios_commands.SecuritiesLoadingHandler",
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
            "trade.cli.commands.portfolios_commands.SecuritiesLoadingHandler",
            **{"return_value.handle.return_value.value": True}
        )
        association_mocker = mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioAssociateSecuritiesHandler",
            **{"return_value.handle.return_value.value": True}
        )
        subject.import_from_file(path_to_config)

        securities_mocker.return_value.handle.assert_called_once()
        association_mocker.return_value.handle.assert_called_once()

    def test_writes_message_on_securities_loading_failure(self, subject, mocker, path_to_config, context):
        mocker.patch(
            "trade.cli.commands.portfolios_commands.SecuritiesLoadingHandler",
            **{"return_value.handle.return_value.is_ok.return_value": False}
        )
        association_mocker = mocker.patch(
            "trade.cli.commands.portfolios_commands.PortfolioAssociateSecuritiesHandler",
        )

        subject.import_from_file(path_to_config)

        association_mocker.assert_not_called()
        context.get_context.return_value.console.print.assert_has_calls(
            [call("[red]Failed to load securities information:")]
        )
