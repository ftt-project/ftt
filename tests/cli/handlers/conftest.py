import os
from pathlib import Path

import pytest

from ftt.cli.application_config_dto import ApplicationConfigDTO


@pytest.fixture
def application_config_dto():
    return ApplicationConfigDTO(
        first_run=True,
        platform="linux",
        application_name="ftt-test",
        environment="test",
        root_path=Path(os.path.join(os.getcwd(), Path(".ftt"))),
    )
