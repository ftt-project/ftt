import pytest

from trade.cli.renderers.portfolio_versions.portfolio_versions_list import (
    PortfolioVersionsList,
)


class TestPortfolioVersionsList:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsList

    def test_renders_list(self, subject, portfolio, portfolio_version, mocker, context):
        mocked = mocker.patch(
            "trade.cli.renderers.portfolio_versions.portfolio_versions_list.Table"
        )
        instance = mocked.return_value

        subject(context, [portfolio_version]).render()

        context.console.print.assert_called_once_with(instance)
