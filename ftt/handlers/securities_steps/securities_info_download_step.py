import math
from time import sleep
from typing import List, Any
from urllib.error import HTTPError

import yfinance as yf
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.value_objects import SecurityValueObject


class SecuritiesInfoDownloadStep(AbstractStep):
    key = "securities_info"

    @classmethod
    def process(
        cls, securities: list[schemas.Security]
    ) -> Result[list[schemas.Security], list[str]]:
        results = [cls.__load_security(security) for security in securities]
        if all([result.is_ok() for result in results]):
            securities_info = [result.value for result in results]
            return Ok(securities_info)
        else:
            errors = [result.err() for result in results if result.is_err()]
            return Err(errors)

    @staticmethod
    def __load_security(security: schemas.Security) -> Result[schemas.Security, str]:
        success = False
        max_retries = 5
        retry_count = 0

        while not success:
            try:
                ticker_object = yf.Ticker(security.symbol)
                info = ticker_object.info.copy()
                security.quote_type = info["quoteType"]
                security.sector = info["sector"]
                security.country = info["country"]
                security.currency = info["currency"]
                security.exchange = info["exchange"]
                security.industry = info["industry"]
                security.short_name = info["shortName"]
                security.long_name = info["longName"]
                success = True

                return Ok(security)

            except HTTPError:
                if retry_count < max_retries:
                    pause_interval = math.pow(2, retry_count)

                    retry_count += retry_count
                    sleep(pause_interval)
                else:
                    return Err(f"Ticker <{security.symbol}> loading exhausted")
            except Exception as e:
                return Err(f"Failed to load ticker <{security.symbol}>: {e}")

        return Err(f"Failed to load ticker <{security.symbol}>")
