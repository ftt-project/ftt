from pathlib import Path
from typing import Optional

from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep


class DefinePackagePathStep(AbstractStep):
    """
    Returns the path to the package.
    Used to read config files that are part of the package.
    """

    key = "package_root_path"

    @classmethod
    def process(cls) -> Result[Path, Optional[str]]:
        import ftt

        path = Path.joinpath(Path(ftt.__file__), Path("..")).resolve()

        return Ok(path)
