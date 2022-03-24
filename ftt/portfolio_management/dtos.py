from dataclasses import dataclass
from typing import Optional

from pandas import DataFrame


@dataclass
class PortfolioAllocationDTO:
    allocation: dict[str, float]
    weights: Optional[dict[str, float]] = None
    leftover: Optional[float] = None
    expected_annual_return: Optional[float] = None
    annual_volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    cov_matrix: Optional[DataFrame] = None
