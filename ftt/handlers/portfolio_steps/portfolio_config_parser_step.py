from datetime import date
from typing import NamedTuple, Optional

import pendulum
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep


class PortfolioConfig(NamedTuple):
    name: str
    budget: float
    symbols: list
    period_start: date
    period_end: date
    interval: str


class PortfolioConfigParserStep(AbstractStep):
    key = "config"

    @classmethod
    def process(cls, raw_config) -> Result[PortfolioConfig, Optional[list]]:
        keys = ["name", "budget", "symbols", "period_start", "period_end", "interval"]
        errors = []
        for k in keys:
            if k not in raw_config:
                errors.append(f"`{k}` is missing from config")

        if "symbols" in raw_config and not isinstance(raw_config["symbols"], list):
            errors.append("`symbols` must be a list")

        if len(errors) > 0:
            return Err(errors)

        if isinstance(raw_config["period_start"], str):
            raw_config["period_start"] = pendulum.parse(raw_config["period_start"])

        if isinstance(raw_config["period_end"], str):
            raw_config["period_end"] = pendulum.parse(raw_config["period_end"])

        return Ok(PortfolioConfig(**raw_config))
