import pytest

from ftt.handlers.securities_steps.securities_load_step import SecuritiesLoadStep


class TestSecuritiesLoadStep:
    @pytest.fixture
    def subject(self):
        return SecuritiesLoadStep

    def test_process_return_list_of_securities(self, subject, security):
        result = subject.process(security_symbols=[security.symbol])

        assert result.is_ok()
        assert isinstance(result.value, list)
        assert len(result.value) > 0
        assert result.value[0].symbol == security.symbol

    def test_process_errors_when_security_does_not_exist(self, subject):
        result = subject.process(security_symbols=['ABC', "CDE"])

        assert result.is_err()
        assert result.value == "Security ABC does not exist; Security CDE does not exist"
