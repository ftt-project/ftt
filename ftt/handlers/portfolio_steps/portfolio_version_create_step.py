from datetime import datetime

from result import Err, Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionCreateStep(AbstractStep):
    key = "portfolio_version"

    ACCEPTABLE_INTERVALS = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]

    @classmethod
    def process(
        cls,
        version: int,
        portfolio: Portfolio,
        amount: float,
        period_start: datetime,
        period_end: datetime,
        interval: str,
    ) -> OkErr:
        if interval not in cls.ACCEPTABLE_INTERVALS:
            return Err(
                f"Interval must be one of {cls.ACCEPTABLE_INTERVALS} but given {interval}."
            )

        if period_end <= period_start:
            return Err(
                "Period end must be greater than period start but given"
                f" period start: {period_start} and period_end {period_end}"
            )

        result = PortfolioVersionsRepository.create(
            version=version,
            portfolio_id=portfolio.id,
            amount=amount,
            period_start=period_start,
            period_end=period_end,
            interval=interval,
        )
        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
