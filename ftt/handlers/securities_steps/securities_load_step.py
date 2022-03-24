from typing import List

import peewee
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesLoadStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(cls, security_symbols: List[str]) -> Result[list, str]:
        results: list[Result] = []
        for security_symbol in security_symbols:
            try:
                result = SecuritiesRepository.get_by_name(security_symbol)
                results.append(Ok(result))
            # TODO move exception handling to the level of repository
            except peewee.DoesNotExist:
                results.append(Err(f"Security {security_symbol} does not exist"))

        if all([result.is_ok() for result in results]):
            return Ok([result.value for result in results])
        else:
            return Err(
                "; ".join([result.value for result in results if result.is_err()])
            )
