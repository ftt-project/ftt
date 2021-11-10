from datetime import datetime

from ftt.logger import logger
from ftt.piloting.scraper import TickersScraper
from ftt.piloting.services.exchange_name_normalizer import ExchangeNameNormalizer
from ftt.storage.models.security import Security


class TickerDataPersister:
    """
    Receives tickers data to persist
    """

    def __init__(self, ticker, scraper=TickersScraper):
        """
        # TODO: refactor, do not accept scraper, accept data to persist
        """
        self.ticker = ticker.strip()
        self.scraper = scraper

    def perform(self):
        db_request = Security.select().where(Security.symbol == self.ticker)
        logger.debug(f"Request: {db_request}")
        if db_request.count() > 0:
            logger.warning(
                (
                    f"Possible duplication of <{self.ticker}> in "
                    "<{db_request[0]} {db_request[0].ticker}:{db_request[0].exchange}>"
                )
            )
            return db_request[0]

        info = self.scraper.load(self.ticker)

        inst, created = Security.get_or_create(
            symbol=self.ticker,
            exchange=info["exchange"],
            defaults={
                "company_name": info["longName"],
                "exchange_name": ExchangeNameNormalizer(info["exchange"]).perform(),
                "type": "?",
                "type_display": info["type"],
                "industry": info["industry"] if "industry" in info else None,
                "currency": info["currency"],
                "updated_at": datetime.now(),
            },
        )
        if created:
            logger.info(f"Ticker loaded: <{inst}>")
            return inst