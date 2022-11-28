import pytest

from ftt.handlers.portfolio_version_associate_securities_hanlder import (
    PortfolioVersionAssociateSecuritiesHandler,
)
from ftt.storage.value_objects import SecurityValueObject


class TestPortfolioVersionAssociateSecuritiesHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionAssociateSecuritiesHandler()

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
