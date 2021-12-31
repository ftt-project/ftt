import pytest

from ftt.handlers.handler.return_result import ReturnResult


class TestReturnResult:
    @pytest.fixture
    def subject(self):
        return ReturnResult

    def test_return_one_key(self, subject):
        input = {"a:": 1, "b": 2}
        result = subject.process(input=input)

        assert result.is_ok()
        assert result.value == input
