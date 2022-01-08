from typing import List, Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Security
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesUpsertStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(
        cls, securities_info: List[dict]
    ) -> Result[List[Security], Optional[str]]:
        results = list(map(SecuritiesRepository.upsert, securities_info))
        results = [record for record, _ in results]
        return Ok(results)
