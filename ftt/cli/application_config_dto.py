import pathlib
from dataclasses import dataclass
from typing import Optional


@dataclass
class ApplicationConfigDTO:
    platform: str
    environment: str
    application_name: str
    root_path: pathlib.Path
    first_run: Optional[bool] = None
