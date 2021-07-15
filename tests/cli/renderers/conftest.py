import pytest


@pytest.fixture
def context(mocker):
    m = mocker.Mock()
    return m