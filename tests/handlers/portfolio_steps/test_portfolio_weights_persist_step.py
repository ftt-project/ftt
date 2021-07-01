import pytest

from trade.handlers.portfolio_steps.test_portfolio_weights_persist_step import PortfolioWeightsPersistStep
from trade.storage.models import Weight


class TestPortfolioWeightsPersistStep:
    @pytest.fixture
    def subject(self):
        return PortfolioWeightsPersistStep

    @pytest.fixture
    def data(self, security):
        return (
            {security.symbol: 80},
            25.599999999998545,
        )

    def test_persist_weights(self, subject, data, portfolio_version):
        result = subject.process(portfolio_version, data, True)

        assert result.is_ok()
        assert type(result.value) == list
        assert isinstance(result.value[0], Weight)

    def test_persist_weights_is_false(self, subject, data, portfolio_version):
        result = subject.process(portfolio_version, data, False)

        assert result.is_ok()
        assert type(result.value) == list
        assert len(result.value) == 0
