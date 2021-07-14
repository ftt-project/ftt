import peewee
import pytest

from trade.cli import renderers
from trade.cli.commands.portfolios_commands import PortfoliosCommands


class TestPortfoliosCommands:
    @pytest.fixture
    def subject(self):
        return PortfoliosCommands()

    def test_list(self, subject, mocker, portfolio):
        context = mocker.patch('trade.cli.commands.portfolios_commands.context')
        context.return_value = mocker.Mock()

        mocker.patch('trade.cli.renderers.PortfoliosList')
        renderers.PortfoliosList.return_value.render.return_value
        subject.list()

        assert type(renderers.PortfoliosList.call_args[0][1]) == list
        assert portfolio in renderers.PortfoliosList.call_args[0][1]
