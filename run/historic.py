import fire
from db.models import Ticker, TickerReturn
import db.configuration as configuration
import db.setup as dbsetup


class Historic:
    """
    Loads historic data from yahoo
    """

    def load_1d_in_5m(self):
        """
        Loads the last day in 5 minutes intervals
        """
        configuration.establish_connection()
        dbsetup.setup_database()

