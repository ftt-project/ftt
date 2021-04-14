from datetime import datetime

from scraper.tickers_scraper import TickersScraper
from trade.db import Ticker
from trade.logger import logger
from trade.services.exchange_name_normalizer import ExchangeNameNormalizer


class TickerDataLoader:
    def __init__(self, ticker, scraper=TickersScraper):
        self.ticker = ticker.strip()
        self.scraper = scraper

    def perform(self):
        db_request = Ticker.select().where(Ticker.ticker == self.ticker)
        logger.debug(f"Request: {db_request}")
        if db_request.count() > 0:
            logger.warning(
                f"Possible duplication of <{self.ticker}> in <{db_request[0]} {db_request[0].ticker}:{db_request[0].exchange}>"
            )
            return db_request[0]

        info = self.scraper.load(self.ticker)

        inst, created = Ticker.get_or_create(
            ticker=self.ticker,
            exchange=info["exchange"],
            defaults={
                "company_name": info["longName"],
                "exchange_name": ExchangeNameNormalizer(info["exchange"]).perform(),
                "type": "?",
                "type_display": info["quoteType"],
                "industry": info["industry"] if "industry" in info else None,
                "currency": info["currency"],
                "updated_at": datetime.now(),
            },
        )
        if created:
            logger.info(f"Ticker loaded: <{inst}>")
            return inst
