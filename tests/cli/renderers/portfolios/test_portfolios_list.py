import pytest

from trade.cli.renderers.portfolios.portfolios_list import PortfoliosList


class TestPortfoliosList:
    @pytest.fixture
    def subject(self):
        return PortfoliosList

    def test_renders_table(self, subject, context, portfolio, mocker):
        mocked = mocker.patch('trade.cli.renderers.portfolios.portfolios_list.Table')
        instance = mocked.return_value

        subject(context, [portfolio]).render()

        context.console.print.assert_called_once_with(instance)
