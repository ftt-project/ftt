import csv
import glob
from datetime import datetime

import chime
import fire
import os

from trade.base_command import BaseCommand
from trade.logger import logger
import pickle

from trade.repositories import TickersRepository
from trade.scraper import TickersScraper

from trade.models import Ticker
import trade.models as configuration

chime.theme("big-sur")


class TickerProgressTracker:
    @staticmethod
    def safe(data, filename="progress.pickle"):
        with open(filename, "wb") as f:
            pickle.dump(data, file=f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename="progress.pickle"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []


class Tickers(BaseCommand):
    """
    Script that requests information about tickers and saves in DB
    """

    def generic(self):
        """
        Parses files from data folder and persist them using db.models.Ticker model
        TODO: Refactor and remove me
        """
        # configuration.establish_connection()

        with open(os.path.join(os.getcwd(), "data", "generic.csv"), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                    continue
                Ticker.create(
                    ticker=row[0],
                    company_name=row[1],
                    exchange=row[2],
                    exchange_name=row[3],
                    type=row[4],
                    type_display=row[5],
                    updated_at=datetime.now(),
                )

        imported_records_count = Ticker.select().count()
        print(f"Imported {imported_records_count} records")

    def remove_ticker_from_progress(self, ticker):
        """
        Remove particular ticker from progress pickle file
        TODO: Refactor and remove me
        """
        saved = TickerProgressTracker.load()
        saved.remove(ticker)
        TickerProgressTracker.safe(saved)

    def find_ticker(self, ticker):
        """
        Load ticker from yahoo finance if it does not exist in database
        """
        ticker = ticker.strip()
        result = TickersScraper.load(ticker)
        if not result:
            logger.warning(f"No ticker found '{ticker}'")
            return
        repository = TickersRepository()
        repository.upsert(result)

    def exchange_lists(self, exchange="ALL"):
        """
        Because `find` method is missing some tickers this method uses eoddata.com data
        to double check NYSE and TSX stocks
        """
        configuration.establish_connection()
        dbsetup.setup_database()

        mask = "*.txt"
        if exchange != "ALL":
            mask = f"{exchange}.txt"

        created_num = 0
        for filename in glob.glob(os.path.join(os.getcwd(), "data", mask)):
            with open(os.path.join(os.getcwd(), "data", filename), "r") as f:
                logger.info(f"Processing {filename} file")
                lines = f.readlines()
                exchange = os.path.basename(filename).split(".")[0]
                not_loaded_tickers = TickerProgressTracker.load()

                for line in lines:
                    line_data = line.split(maxsplit=1)
                    ticker = line_data[0].strip()
                    ticker = self.__normalize_ticker(ticker, exchange)

                    db_request = Ticker.select().where(
                        Ticker.symbol == ticker, Ticker.exchange == exchange
                    )
                    logger.debug(f"Request: {db_request}")
                    if db_request.count() > 0:
                        continue

                    if ticker in not_loaded_tickers:
                        logger.debug(
                            f"Found in skipped table <{ticker}> in <{exchange}>. Skipping"
                        )
                        continue

                    logger.info(f"Missing ticker detected: <{ticker}> in <{exchange}>")

                    info = TickersScraper.load(ticker)
                    if not info:
                        not_loaded_tickers.append(ticker)
                        TickerProgressTracker.safe(not_loaded_tickers)
                        logger.debug(f"Skipping {ticker}")
                        continue

                    inst, created = Ticker.get_or_create(
                        ticker=ticker,
                        exchange=info["exchange"],
                        defaults={
                            "company_name": info["longName"],
                            "exchange_name": self.__normalize_exchange_name(
                                info["exchange"]
                            ),
                            "type": "?",
                            "type_display": info["quoteType"],
                            "industry": info["industry"]
                            if "industry" in info
                            else None,
                            "currency": info["currency"],
                            "updated_at": datetime.now(),
                        },
                    )
                    logger.info(f"Ticker loaded: <{ticker}> in <{exchange}>")
                    if created:
                        created_num += 1
        logger.info(f"Created {created_num} new ticker records")
        chime.success()

    def __normalize_ticker(self, ticker, exchange):
        """
        TODO: Refactor and remove me
        """
        if exchange == "TOR":
            return f"{ticker}.TO"
        else:
            return ticker

    def __normalize_exchange_name(self, exchange_name):
        """
        TODO: Refactor and remove me
        """
        if exchange_name == "TOR":
            return "Toronto"
        elif exchange_name == "NCM":
            return "NASDAQ"
        elif exchange_name == "NYQ":
            return "NYSE"
        else:
            return exchange_name


if __name__ == "__main__":
    try:
        fire.Fire({
            "find_ticker": Tickers().find_ticker
        })
    except Exception as e:
        chime.error()
        raise e
