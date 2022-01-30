from pathlib import Path
from typing import Optional

from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep


class DefineExampleConfigPathStep(AbstractStep):
    """
    Returns the path to the example config file.
    """

    key = "example_config_path"

    @classmethod
    def process(cls, package_root_path: Path) -> Result[Path, Optional[str]]:
        path = package_root_path.joinpath(Path("config"), Path("example_portfolio.yml"))

        return Ok(path)
