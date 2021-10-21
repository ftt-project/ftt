import pytest

from ftt.cli.renderers.securities.securities_list import SecuritiesList


class TestSecuritiesList:
    @pytest.fixture
    def subject(self):
        return SecuritiesList

    def test_renders_list(self, subject, mocker, context, security):
        mocked = mocker.patch("ftt.cli.renderers.securities.securities_list.Table")
        instance = mocked.return_value

        subject(context, [security]).render()

        context.console.print.assert_called_once_with(instance)
