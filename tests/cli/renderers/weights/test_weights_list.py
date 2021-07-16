import pytest

from trade.cli.renderers.weights.weights_list import WeightsList


class TestWeightsList:
    @pytest.fixture
    def subject(self):
        return WeightsList

    def test_renders_list(self, subject, context, mocker, portfolio, portfolio_version, security, weight):
        mocked = mocker.patch('trade.cli.renderers.weights.weights_list.Table')
        instance = mocked.return_value

        subject(context, [weight]).render()

        context.console.print.assert_called_once_with(instance)
