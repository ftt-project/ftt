from collections import namedtuple

import pytest


@pytest.fixture
def config():
    dictionary = {"host": "127.0.0.1", "port": 4002, "client_id": 1234}
    return namedtuple("Config", dictionary.keys())(*dictionary.values())
