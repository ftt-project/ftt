import pytest


@pytest.fixture
def context(mocker):
    context = mocker.Mock()
    context.__enter__ = mocker.Mock(return_value=(mocker.Mock(), None))
    context.__exit__ = mocker.Mock(return_value=None)

    console = mocker.Mock()
    console.status.return_value = context

    m = mocker.Mock()
    m.get_context.return_value.console = console
    return m
