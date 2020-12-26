from collections import namedtuple

import yaml


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
        return namedtuple("Scrape", configuration["scrape"].keys())(
            **configuration["scrape"]
        )

    def __read_config(self):
        with open(Configuration.FILE) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
