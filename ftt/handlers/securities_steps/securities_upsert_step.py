from typing import List

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesUpsertStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(
        cls, securities_info: List[schemas.Security]
    ) -> Result[List[schemas.Security], str]:
        upserted_result: list[tuple[schemas.Security, bool]] = list(
            map(SecuritiesRepository.upsert, securities_info)
        )
        results: list[schemas.Security] = [record for record, _ in upserted_result]
        return Ok(results)
