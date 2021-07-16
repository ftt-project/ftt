import pytest


@pytest.fixture
def context(mocker):
    m = mocker.Mock()
    m.get_context.return_value.console
    return m