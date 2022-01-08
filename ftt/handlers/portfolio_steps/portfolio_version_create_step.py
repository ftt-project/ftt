from datetime import datetime
from typing import Optional

from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import ACCEPTABLE_INTERVALS, PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionCreateStep(AbstractStep):
    key = "portfolio_version"

    @classmethod
    def process(
        cls,
        version: int,
        portfolio: Portfolio,
        value: float,
        period_start: datetime,
        period_end: datetime,
        interval: str,
    ) -> Result[PortfolioVersion, Optional[str]]:
        if interval not in ACCEPTABLE_INTERVALS:
            return Err(
                f"Interval must be one of {ACCEPTABLE_INTERVALS} but given {interval}."
            )

        if period_end <= period_start:
            return Err(
                "Period end must be greater than period start but given"
                f" period start: {period_start} and period_end {period_end}"
            )

        result = PortfolioVersionsRepository.create(
            version=version,
            portfolio_id=portfolio.id,
            value=value,
            period_start=period_start,
            period_end=period_end,
            interval=interval,
        )
        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
