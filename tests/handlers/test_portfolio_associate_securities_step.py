import pytest

from ftt.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from ftt.storage.data_objects.security_dto import SecurityValueObject


class TestPortfolioAssociateSecuritiesHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioAssociateSecuritiesHandler()

    def test_associates_portfolio_with_securities(
        self, subject, portfolio, portfolio_version, security
    ):
        result = subject.handle(
            securities=[SecurityValueObject(symbol=security.symbol)],
            portfolio_version=portfolio_version,
        )

        assert result.is_ok()
        assert result.value == portfolio_version
        assert result.value.weights == [security]
