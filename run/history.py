import fire

from trade.base_command import BaseCommand
import chime

from scraper.history_scraper import HistoryScraper
from trade.logger import logger
from trade.configuration import Configuration
from db.models import Ticker, TickerReturn

chime.theme("big-sur")


class History(BaseCommand):
    """
    Loads historic data from yahoo
    """

    def load_all(self, exchange, offset=0):
        tickers_query = (
            Ticker.select(Ticker.ticker)
            .where(Ticker.exchange == exchange)
            .order_by(Ticker.ticker)
        )
        if tickers_query.count() == 0:
            self.log_warning(f"No tickers found for <{exchange}>")
            return

        limit = 10
        tickers_batch = tickers_query.limit(limit).offset(offset)
        while tickers_batch.count() > 0:
            tickers = [ticker.ticker for ticker in tickers_batch]

            inserted_num = self.load(tickers)
            self.log_info(
                f"Processed <{len(tickers)}> tickers. Loaded {inserted_num} historic records. Offset <{offset}>. The last is {tickers[-1]}"
            )

            offset += limit
            tickers_batch = tickers_query.limit(limit).offset(offset)

    def load(self, ticker="ALL"):
        """
        :param: ticker optionally specify ticker to load
        """

        config = Configuration().scrape()
        if ticker != "ALL":
            if isinstance(ticker, str):
                config.tickers = [ticker]
            elif isinstance(ticker, list):
                config.tickers = ticker
            else:
                raise ValueError(
                    f"Unknown type {type(ticker)}. Must be `str` or `list`"
                )

        data_frame = HistoryScraper.load(config)
        if len(config.tickers) == 1:
            grouped_by_ticker = {config.tickers[0]: data_frame}
        else:
            grouped_by_ticker = {
                idx: data_frame.xs(idx, level=1, axis=1)
                for idx, gp in data_frame.groupby(level=1, axis=1)
            }

        created_num = 0
        for ticker_name in grouped_by_ticker.keys():
            self.log_info(f"Loading <{ticker_name}> ...")
            ticker_data = grouped_by_ticker[ticker_name]
            ticker_data = ticker_data[ticker_data["Close"].notnull()]
            before = TickerReturn.select().count()
            for index, row in ticker_data.iterrows():
                ins = (
                    TickerReturn.insert(
                        ticker=Ticker.get(ticker=ticker_name),
                        datetime=index,
                        interval=config.interval,
                        open=row["Open"],
                        high=row["High"],
                        low=row["Low"],
                        close=row["Close"],
                        volume=row["Volume"],
                        change=row["Close"] - row["Open"],
                        percent_change=round(
                            (row["Close"] - row["Open"]) / row["Close"] * 100, 5
                        ),
                    )
                    .on_conflict_ignore()
                    .execute()
                )
            after = TickerReturn.select().count()
            created_num += after - before
            self.log_info(f"Loaded <{ticker_name}> history data")

        logger.info(
            f"Created {created_num} records for {config.tickers} <{config.interval_start}>:<{config.interval_end}> with interval <{config.interval}>"
        )
        chime.success()
        return created_num


if __name__ == "__main__":
    fire.Fire(History)
