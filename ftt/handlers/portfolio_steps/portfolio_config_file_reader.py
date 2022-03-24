from typing import Optional

import yaml  # type: ignore
from result import Err, Ok, Result
from yaml.scanner import ScannerError  # type: ignore

from ftt.handlers.handler.abstract_step import AbstractStep


class PortfolioConfigFileReaderStep(AbstractStep):
    key = "raw_config"

    @classmethod
    def process(cls, example_config_path: str) -> Result[dict, Optional[Exception]]:
        try:
            stream = open(example_config_path, "r")
            config = yaml.safe_load(stream)
            return Ok(config)
        except FileNotFoundError as e:
            return Err(e)
        except ScannerError as e:
            return Err(e)
