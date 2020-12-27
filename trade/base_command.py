import chime
from abc import ABC

import db.configuration as configuration
import db.setup as dbsetup
from trade.logger import logger


class BaseCommand(ABC):
    def __init__(self):
        configuration.establish_connection()
        dbsetup.setup_database()

    def debug(self, message):
        logger.debug(message)

    def log_info(self, message):
        pass

    def log_warning(self, message):
        pass

    def failed(self, message):
        pass

    def success(self, message: str) -> None:
        """
        :param message: Success message to print
        :return: None
        """
        logger.info(message)
        chime.success()

