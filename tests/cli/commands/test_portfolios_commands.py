from unittest.mock import call

import peewee
import pytest

from trade.cli import renderers
from trade.cli.commands.portfolios_commands import PortfoliosCommands


class TestPortfoliosCommands:
    @pytest.fixture
    def subject(self):
        return PortfoliosCommands()

    def test_list(self, subject, mocker):
        mocker.patch('trade.cli.renderers.PortfoliosList')
        obj = mocker.Mock()
        renderers.PortfoliosList.return_value = obj
        subject.list()

        assert type(renderers.PortfoliosList.call_args[0][1]) == peewee.ModelObjectCursorWrapper
        obj.render.assert_called_once()

