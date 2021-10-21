from typing import Dict

import pandas as pd
from result import Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.mappers.security_price_mapper import SecurityPriceMapper
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.security_prices_repository import SecurityPricesRepository


class SecurityPricesUpsertStep(AbstractStep):
    key = "security_prices"

    @classmethod
    def process(
        cls, security_prices_data: Dict[str, pd.DataFrame], interval: str
    ) -> OkErr:
        mapped_data = [
            (symbol, SecurityPriceMapper.from_dataframe(dataframe).to_dicts())
            for symbol, dataframe in security_prices_data.items()
        ]

        results = {}
        for symbol, price_changes in mapped_data:
            security = SecuritiesRepository.get_by_name(symbol)
            new_rows = 0
            for row in price_changes:
                row["security"] = security
                row["interval"] = interval
                record, flag = SecurityPricesRepository.upsert(row)
                if flag:
                    new_rows += 1
                # TODO: handle upsert errors
            results[symbol] = new_rows

        return Ok(results)
