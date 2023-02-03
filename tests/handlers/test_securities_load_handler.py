import pytest

from ftt.handlers.securities_handler import SecuritiesLoadHandler


class TestSecuritiesLoadHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesLoadHandler
