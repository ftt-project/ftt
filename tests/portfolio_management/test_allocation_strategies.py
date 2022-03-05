import pandas as pd
import pytest

from ftt.portfolio_management.dtos import PortfolioAllocationDTO
from ftt.portfolio_management.allocation_strategies import DefaultAllocationStrategy


class TestDefaultAllocationStrategy:
    @pytest.fixture
    def subject(self):
        return DefaultAllocationStrategy

    def test_allocate_returns_dto_with_allocation(self, subject):
        dto = PortfolioAllocationDTO(
            weights={
                "A": 0.5,
                "B": 0.2,
                "C": 0.3,
            },
            cov_matrix=pd.DataFrame(
                data={
                    "A": [1, 2, 3],
                    "B": [4, 5, 6],
                    "C": [7, 8, 9],
                },
                index=["A", "B", "C"],
            ),
        )

        latest_prices = {
            "A": 113,
            "B": 25,
            "C": 271,
        }

        result = subject(
            allocation_dto=dto, value=10005, latest_prices=latest_prices
        ).allocate()

        assert result == dto
        assert dto.leftover == 27.0
        assert dto.allocation == {"A": 44, "B": 81, "C": 11}
        assert dto.expected_annual_return == 142.8
        assert round(dto.annual_volatility, 3) == 2.049
        assert dto.sharpe_ratio is None

    def test_allocate_returns_allocation_with_weights_gt_zero(self, subject):
        dto = PortfolioAllocationDTO(
            weights={
                "A": 0.5,
                "B": 0,
                "C": 0.3,
            },
            cov_matrix=pd.DataFrame(
                data={
                    "A": [1, 2, 3],
                    "B": [4, 5, 6],
                    "C": [7, 8, 9],
                },
                index=["A", "B", "C"],
            ),
        )

        latest_prices = {
            "A": 113,
            "B": 25,
            "C": 271,
        }

        _ = subject(
            allocation_dto=dto, value=10005, latest_prices=latest_prices
        ).allocate()

        assert dto.allocation == {"A": 45, "B": 0, "C": 12}
