import fire
import peewee

from trade.logger import logger
import chime

from scraper.history_scraper import HistoryScraper
from trade.logger import logger
from trade.configuration import Configuration
from db.models import Ticker, TickerReturn
import db.configuration as configuration
import db.setup as dbsetup

chime.theme("big-sur")


class History:
    """
    Loads historic data from yahoo
    """

    def load(self, ticker="ALL"):
        """
        :param: ticker optionally specify ticker to load
        """
        configuration.establish_connection()
        dbsetup.setup_database()

        config = Configuration().scrape()
        if ticker != "ALL":
            config.tickers = [ticker]

        data_frame = HistoryScraper.load(config)
        if len(config.tickers) == 1:
            grouped_by_ticker = {
                config.tickers[0]: data_frame
            }
        else:
            grouped_by_ticker = {idx: data_frame.xs(idx, level=1, axis=1) for idx, gp in
                                 data_frame.groupby(level=1, axis=1)}

        for ticker_name in grouped_by_ticker.keys():
            ticker_data = grouped_by_ticker[ticker_name]
            ticker_data = ticker_data[ticker_data['Close'].notnull()]
            created_num = 0
            for index, row in ticker_data.iterrows():
                ins, created = TickerReturn.get_or_create(
                    ticker=Ticker.get(ticker=ticker_name),
                    datetime=index,
                    interval=config.interval,
                    defaults={
                        "open": row["Open"],
                        "high": row["High"],
                        "low": row["Low"],
                        "close": row["Close"],
                        "volume": row["Volume"],
                        "change": row["Close"] - row["Open"],
                        "percent_change": (row["Close"] - row["Open"]) / row["Close"] * 100
                    }
                )
                if created:
                    created_num += 1

        logger.info(
            f"Created {created_num} records for {config.tickers} <{config.interval_start}>:<{config.interval_end}> with interval <{config.interval}>"
        )
        chime.success()


if __name__ == "__main__":
    fire.Fire(History)
