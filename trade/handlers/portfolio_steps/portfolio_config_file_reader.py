import yaml
from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep


class PortfolioConfigFileReaderStep(AbstractStep):
    key = "raw_config"

    @classmethod
    def process(cls, path: str) -> OkErr:
        try:
            stream = open(path, "r")
            config = yaml.safe_load(stream)
            return Ok(config)
        except FileNotFoundError as e:
            return Err(e)
        except yaml.scanner.ScannerError as e:
            return Err(e)
