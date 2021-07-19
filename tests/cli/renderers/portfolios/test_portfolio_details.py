import pytest

from trade.cli.renderers.portfolios.portfolio_details import PortfolioDetails


class TestPortfolioDetails:
    @pytest.fixture
    def subject(self):
        return PortfolioDetails

    def test_renders_portfolio(self, subject, mocker, context, portfolio):
        mocked = mocker.patch("trade.cli.renderers.portfolios.portfolio_details.Table")
        instance = mocked.return_value

        subject(context, portfolio).render()

        context.console.print.assert_called_once_with(instance)
