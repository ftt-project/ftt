import pytest

from ftt.handlers.position_steps.compare_planned_actual_positions_step import (
    ComparePlannedActualPositionsStep,
)
from ftt.storage import schemas


class TestComparePlannedActualPositionsStep:
    @pytest.fixture
    def subject(self):
        return ComparePlannedActualPositionsStep

    @pytest.fixture
    def position(self):
        def _position(position, symbol):
            return schemas.Position(
                account="acc1",
                contract=schemas.Contract(
                    symbol=symbol,
                ),
                position=position,
            )

        return _position

    def test_returns_nothing_if_no_action_required(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-2"), 20, 20
                ),
            ],
            [
                position(10, "AA-1"),
                position(20, "AA-2"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 0

    def test_returns_combination_order_contract_with_sell_action(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
            ],
            [
                position(20, "AA-1"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 1
        assert type(result.value[0]) == schemas.CalculatedPositionDifference
        assert (
            result.value[0].actual_position_difference
            == schemas.CalculatedPositionDifference.Difference.BIGGER
        )
        assert result.value[0].delta == 10
        assert result.value[0].planned_position == 10.0
        assert result.value[0].actual_position == 20.0
        assert result.value[0].symbol == "AA-1"

    def test_returns_combination_order_contract_with_buy_action(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
            ],
            [
                position(5, "AA-1"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 1
        assert (
            result.value[0].actual_position_difference
            == schemas.CalculatedPositionDifference.Difference.SMALLER
        )
        assert result.value[0].delta == 5
        assert result.value[0].symbol == "AA-1"
        assert result.value[0].planned_position == 10.0
        assert result.value[0].actual_position == 5.0

    def test_returns_combination_order_contract_with_sell_buy_actions(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-2"), 10, 10
                ),
            ],
            [
                position(5, "AA-1"),
                position(17, "AA-2"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 2

        sell_position = list(
            filter(
                lambda value: value.actual_position_difference
                == schemas.CalculatedPositionDifference.Difference.BIGGER,
                result.value,
            )
        )[0]
        assert sell_position.delta == 7.0
        assert sell_position.symbol == "AA-2"

        buy_position = list(
            filter(
                lambda value: value.actual_position_difference
                == schemas.CalculatedPositionDifference.Difference.SMALLER,
                result.value,
            )
        )[0]
        assert buy_position.delta == 5.0
        assert buy_position.symbol == "AA-1"

    def test_returns_no_actions_required_ignores_positions_not_in_portfolio(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
            ],
            [
                position(10, "AA-1"),
                position(17, "AA-2"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 0

    def test_returns_combination_buy_order_contract_with_no_positions(
        self, subject, weight_factory, portfolio_version, security_factory, position
    ):
        result = subject.process(
            [
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-1"), 10, 10
                ),
                weight_factory(
                    portfolio_version, security_factory(symbol="AA-2"), 10, 10
                ),
            ],
            [
                position(10, "AA-1"),
            ],
        )

        assert result.is_ok()
        assert len(result.value) == 1

        assert (
            result.value[0].actual_position_difference
            == schemas.CalculatedPositionDifference.Difference.SMALLER
        )
        assert result.value[0].delta == 10.0
        assert result.value[0].symbol == "AA-2"
