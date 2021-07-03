from typing import List

from result import Ok

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.repositories import SecuritiesRepository


class SecuritiesUpsertStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(cls, securities_info: List[dict]):
        results = list(map(SecuritiesRepository.upsert, securities_info))
        results = [record for record, _ in results]
        return Ok(results)
