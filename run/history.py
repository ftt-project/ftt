import fire

from scraper.history_scraper import HistoryScraper
from trade.logger import logger


from trade.configuration import Configuration
from db.models import Ticker, TickerReturn
import db.configuration as configuration
import db.setup as dbsetup


class History:
    """
    Loads historic data from yahoo
    """
    def load(self, ticker="ALL"):
        """
        Loads the last day in 5 minutes intervals
        """
        configuration.establish_connection()
        dbsetup.setup_database()

        config = Configuration().scrape()
        historical_data = HistoryScraper.load(config)
        # r1 = data.iloc[1]
        # Adj Close  AC.TO    4.254000e+01
        #            QQQ      1.826122e+02
        #            SHOP     3.103600e+02
        # Close      AC.TO    4.254000e+01
        #            QQQ      1.840500e+02
        #            SHOP     3.103600e+02
        # High       AC.TO    4.320000e+01
        #            QQQ      1.860300e+02
        #            SHOP     3.111700e+02
        # Low        AC.TO    4.180000e+01
        #            QQQ      1.830200e+02
        #            SHOP     3.007000e+02
        # Open       AC.TO    4.278000e+01
        #            QQQ      1.860000e+02
        #            SHOP     3.096400e+02
        # Volume     AC.TO    1.690844e+06
        #            QQQ      4.854430e+07
        #            SHOP     2.206200e+06
        # ------
        # r1.index
        # MultiIndex([('Adj Close', 'AC.TO'),
        #             ('Adj Close', 'QQQ'),
        #             ('Adj Close', 'SHOP'),
        #             ('Close', 'AC.TO'),
        #             ('Close', 'QQQ'),
        #             ('Close', 'SHOP'),
        #             ('High', 'AC.TO'),
        #             ('High', 'QQQ'),
        #             ('High', 'SHOP'),
        #             ('Low', 'AC.TO'),
        #             ('Low', 'QQQ'),
        #             ('Low', 'SHOP'),
        #             ('Open', 'AC.TO'),
        #             ('Open', 'QQQ'),
        #             ('Open', 'SHOP'),
        #             ('Volume', 'AC.TO'),
        #             ('Volume', 'QQQ'),
        #             ('Volume', 'SHOP')],
        print(historical_data)


if __name__ == '__main__':
    fire.Fire(History)
