from dataclasses import dataclass

import yaml

@dataclass
class Scrape:
    tickers: str
    interval_start: str
    interval_end: str
    interval: str


class Configuration:
    FILE = "config/symbols.yml"

    def tickers_to_track(self) -> list:
        """
        :returns: a list of tickers to track
        """
        tickers = set()
        configuration = self.__read_config()
        for symbol in configuration["track"]:
            tickers.append(symbol)

        return tickers

    def scrape(self):
        """
        :returns: a configuration for scraping
        """
        configuration = self.__read_config()
        return Scrape(**configuration["scrape"])

    def __read_config(self):
        with open(Configuration.FILE) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
