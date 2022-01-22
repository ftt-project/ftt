import pytest

from ftt.cli.plugin import Plugin


class TestPlugin:
    @pytest.fixture
    def subject(self):
        return Plugin

    # def test_set_environment(self, subject, mocker):
    #     sys = mocker.patch('ftt.cli.plugin.sys')
    #     sys.argv = ['__main__.py', '--version', '--dev']
    #     sys.exit.return_value = None
    #
    #     parser = subject().get_opts_parser()
    #     argv
    #
    #     assert instance.environment == 'development'
