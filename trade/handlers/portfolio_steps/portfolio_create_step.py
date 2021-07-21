from datetime import datetime

from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioCreateStep(AbstractStep):
    key = "portfolio"

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
        name: str,
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

        result = PortfoliosRepository.create(
            name=name,
            amount=amount,
            period_start=period_start,
            period_end=period_end,
            interval=interval,
        )

        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
