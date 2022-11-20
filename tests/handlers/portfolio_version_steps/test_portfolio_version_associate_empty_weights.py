import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_associate_empty_weights_step import (
    PortfolioVersionAssociateEmptyWeightsStep,
)
from ftt.storage.data_objects.security_dto import SecurityValueObject


class TestPortfolioVersionAssociateEmptyWeights:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionAssociateEmptyWeightsStep

    def test_process_associates_empty_weights_with_portfolio_version(
        self, subject, security, portfolio_version
    ):
        result = subject.process(
            securities=[SecurityValueObject(symbol=security.symbol)],
            portfolio_version=portfolio_version,
        )

        assert result.is_ok()
        assert len(result.value) == 1
        assert portfolio_version.weights == result.value[0]
