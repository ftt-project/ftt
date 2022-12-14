import pytest

from ftt.handlers.weighted_securities_steps.combine_weighted_securities_step import (
    CombineWeightedSecuritiesStep,
)
from ftt.storage import schemas


class TestCombineWeightedSecuritiesStep:
    @pytest.fixture
    def subject(self):
        return CombineWeightedSecuritiesStep

    def test_returns_combined_weighted_securities(
        self,
        subject,
        weighted_security_factory,
        security_factory,
        portfolio_factory,
        portfolio_version_factory,
    ):
        s1 = security_factory(symbol="AAPL1")
        p1 = portfolio_factory(name="Portfolio1")
        pv1 = portfolio_version_factory(portfolio=p1)
        w1 = weighted_security_factory(
            security=s1,
            portfolio=p1,
            portfolio_version=pv1,
            position=None,
            planned_position=None,
            amount=None,
        )
        w2 = weighted_security_factory(security=s1, portfolio=p1, portfolio_version=pv1)

        result = subject.process(
            portfolio_weighted_securities=[w1],
            portfolio_version_weighted_securities=[w2],
        )

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert len(result.value) == 1
        assert result.value[0].symbol == w2.symbol
        assert result.value[0].security == w2.security
        assert result.value[0].position == w2.position
        assert result.value[0].planned_position == w2.planned_position
        assert result.value[0].amount == w2.amount
        assert result.value[0].portfolio_version.id == w2.portfolio_version.id
        assert result.value[0].portfolio.id == w2.portfolio.id
        assert result.value[0].weighted
        assert not result.value[0].discarded

    def test_returns_combined_weighted_securities_and_mark_unweighted(
        self,
        subject,
        weighted_security_factory,
        security_factory,
        portfolio_factory,
        portfolio_version_factory,
    ):
        s1 = security_factory(symbol="AAPL2")
        p1 = portfolio_factory(name="Portfolio2")
        pv1 = portfolio_version_factory(portfolio=p1)
        w1 = weighted_security_factory(
            security=s1,
            portfolio=p1,
            portfolio_version=pv1,
            position=None,
            planned_position=None,
            amount=None,
        )

        result = subject.process(
            portfolio_weighted_securities=[w1], portfolio_version_weighted_securities=[]
        )

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert len(result.value) == 1
        assert result.value[0].symbol == w1.symbol
        assert not result.value[0].weighted

    def test_returns_combined_weighted_securities_and_mark_discarded(
        self,
        subject,
        weighted_security_factory,
        security_factory,
        portfolio_factory,
        portfolio_version_factory,
    ):
        s1 = security_factory(symbol="AAPL2")
        p1 = portfolio_factory(name="Portfolio2")
        pv1 = portfolio_version_factory(portfolio=p1)
        w1 = weighted_security_factory(
            security=s1,
            portfolio=p1,
            portfolio_version=pv1,
            position=None,
            planned_position=None,
            amount=None,
        )

        result = subject.process(
            portfolio_weighted_securities=[], portfolio_version_weighted_securities=[w1]
        )

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert len(result.value) == 1
        assert result.value[0].symbol == w1.symbol
        assert result.value[0].discarded
