import pytest

from ftt.cli.renderers.portfolio_versions.portfolio_version_details import (
    PortfolioVersionDetails,
)


class TestPortfolioVersionDetails:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDetails

    def test_renders_details(
        self, subject, portfolio, portfolio_version, mocker, context
    ):
        mocked = mocker.patch(
            "ftt.cli.renderers.portfolio_versions.portfolio_version_details.Table"
        )
        instance = mocked.return_value

        subject(context, portfolio_version).render()

        context.console.print.assert_called_once_with(instance)
