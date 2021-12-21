import pytest

from ftt.handlers.securities_load_handler import SecuritiesLoadHandler


class TestSecuritiesLoadHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesLoadHandler