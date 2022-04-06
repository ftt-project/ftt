import math
from time import sleep
from typing import List, Any
from urllib.error import HTTPError

import yfinance as yf
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.security_dto import SecurityDTO


class SecuritiesInfoDownloadStep(AbstractStep):
    key = "securities_info"

    @classmethod
    def process(cls, securities: List[SecurityDTO]) -> Result[list, list]:
        results = [cls.__load_security(security) for security in securities]
        if all([result.is_ok() for result in results]):
            securities_info = [result.value for result in results]
            return Ok(securities_info)
        else:
            errors = [result.err() for result in results if result.is_err()]
            return Err(errors)

    @staticmethod
    def __load_security(security: SecurityDTO) -> Result[Any, str]:
        success = False
        max_retries = 5
        retry_count = 0

        while not success:
            try:
                ticker_object = yf.Ticker(security.symbol)
                info = ticker_object.info.copy()
                # TODO move me to mapper
                info["quote_type"] = info.pop("quoteType")
                info["short_name"] = info.pop("shortName")
                info["long_name"] = info.pop("longName")
                success = True
                return Ok(info)

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
