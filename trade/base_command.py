import chime
from abc import ABC

from trade.logger import logger


class BaseCommand(ABC):
    def __init__(self):
        configuration.establish_connection()
        dbsetup.setup_database()

    def debug(self, message):
        logger.debug(message)

    def log_info(self, message):
        logger.info(message)

    def log_warning(self, message):
        logger.warning(message)

    def failed(self, message):
        pass

    def success(self, message: str) -> None:
        """
        :param message: Success message to print
        :return: None
        """
        logger.info(message)
        chime.success()
