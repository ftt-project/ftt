import os
import pathlib

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

    @pytest.mark.skip(reason="Not implemented test")
    def test_fails_to_import_portfolio_and_assets_info_is_not_requested(self, subject):
        pass

    def test_on_correct_config_request_assets_info(
        self, subject, mocker, path_to_config
    ):
        mocked = mocker.patch(
            "trade.cli.commands.portfolios_commands.SecuritiesLoadingHandler",
            **{"return_value.handle.return_value.value": True}
        )
        subject.import_from_file(path_to_config)
        mocked.return_value.handle.assert_called_once()
