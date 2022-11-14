from typing import Optional

import peewee
from result import Result, Err, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import Storage
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioVersionDeleteStep(AbstractStep):
    key = "portfolio_version_delete"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[bool, Optional[str]]:
        if portfolio_version.active:
            return Err("Cannot delete active portfolio version")

        db = Storage.get_database()
        with db.atomic():
            try:
                weights = WeightsRepository.get_by_portfolio_version(portfolio_version)
                for weight in weights:
                    WeightsRepository.delete(weight)
                PortfolioVersionsRepository.delete(portfolio_version)
            except peewee.PeeweeException as e:
                return Err(
                    f"Failed to delete Portfolio version #{portfolio_version.id} due to {e}"
                )

        return Ok(True)
