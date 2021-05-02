import math
import urllib
from time import sleep

import chime
import yfinance as yf

from trade.logger import logger

chime.theme("big-sur")


class TickersScraper:
    class TickerLoadingError(Exception):
        pass

    @staticmethod
    def load(ticker: str):
        success = False
        max_retries = 5
        retry_count = 0

        while not success:
            try:
                ticker_object = yf.Ticker(ticker)
                info = ticker_object.info
                success = True
                return info
            except urllib.error.HTTPError as e:
                if retry_count < max_retries:
                    pause_interval = math.pow(2, retry_count)
                    logger.debug(
                        f"Retry attempt: {retry_count+1}. Sleep period: {pause_interval}"
                    )
                    retry_count += retry_count
                    sleep(pause_interval)
                else:
                    chime.warning()
                    raise TickersScraper.TickerLoadingError(
                        f"Ticker <{ticker}> loading exhausted"
                    )
            except ValueError as e:
                success = True
                logger.error(f"Ticker information not found: <{ticker}>: {e}")
            except (TickersScraper.TickerLoadingError, KeyError, IndexError) as e:
                success = True
                logger.error(f"Failed to load ticker <{ticker}>: {e}")
            except Exception as e:
                chime.error()
                logger.error(f"Failed to load ticker <{ticker}>: {e}")
                raise e
