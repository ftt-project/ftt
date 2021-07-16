import pytest

from trade.cli.commands.portfolios_commands import PortfoliosCommands


class TestPortfoliosCommands:
    @pytest.fixture
    def subject(self):
        return PortfoliosCommands()

    @pytest.fixture(autouse=True)
    def mock_context(self, mocker, context):
        mocker.patch("trade.cli.commands.portfolios_commands.context", new=context)

    def test_list(self, subject, mocker, portfolio):
        mocked = mocker.patch('trade.cli.commands.portfolios_commands.PortfoliosList')
        mocked.return_value.render.return_value
        subject.list()

        assert type(mocked.call_args[0][1]) == list
        assert portfolio in mocked.call_args[0][1]

    def test_details_renders_portfolio_details(self, subject, mocker, portfolio, portfolio_version):
        mocked = mocker.patch('trade.cli.commands.portfolios_commands.PortfolioDetails',
                              **{'return_value.render.return_value': True})
        subject.details(portfolio.id)

        assert portfolio == mocked.call_args[0][1]

    def test_details_renders_portfolio_versions_list(self, subject, mocker, portfolio, portfolio_version):
        mocked = mocker.patch('trade.cli.commands.portfolios_commands.PortfolioVersionsList',
                              **{'return_value.render.return_value': True})
        subject.details(portfolio.id)

        assert portfolio_version in mocked.call_args[0][1]
