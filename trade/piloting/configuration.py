import os
from dataclasses import dataclass

import yaml


@dataclass
class ScrapeConfig:
    tickers: str
    interval_start: str
    interval_end: str
    interval: str


class Configuration:
    FILE = os.path.join(os.path.dirname(__file__), "../../config/symbols.yml")

    def etfs(self) -> set:
        tickers = set()
        configuration = self.__read_config()
        for symbol in configuration["ETFs"]:
            tickers.add(symbol)

        return tickers

    def tickers_to_track(self) -> set:
        """
        :returns: a list of tickers to track
        """
        tickers = set()
        configuration = self.__read_config()
        for symbol in configuration["track"]:
            tickers.add(symbol)

        return tickers

    def scrape(self):
        """
        :returns: a configuration for scraping
        """
        configuration = self.__read_config()
        return ScrapeConfig(**configuration["scrape"])

    def __read_config(self):
        with open(Configuration.FILE) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
