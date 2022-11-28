import pytest

from ftt.handlers.securities_steps.securities_associate_with_portfolio_step import SecuritiesAssociateWithPortfolioStep
from ftt.storage import schemas


class TestSecuritiesAssociateWithPortfolioStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesAssociateWithPortfolioStep

    def test_associates_portfolio_with_securities(self, subject, portfolio, security):
        result = subject.process(
            securities=[schemas.Security.from_orm(security)],
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert result.value == [schemas.Security.from_orm(security)]
