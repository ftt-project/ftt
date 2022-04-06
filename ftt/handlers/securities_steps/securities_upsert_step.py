from typing import List

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Security
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesUpsertStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(cls, securities_info: List[dict]) -> Result[List[Security], str]:
        upserted_result: list[tuple[Security, bool]] = list(
            map(SecuritiesRepository.upsert, securities_info)
        )
        results: list[Security] = [record for record, _ in upserted_result]
        return Ok(results)
