import pytest

from trade.handlers.handler.retrun_result import ReturnResult


class TestReturnResult:
    @pytest.fixture
    def subject(self):
        return ReturnResult

    def test_return_one_key(self, subject):
        input = {"a:": 1, "b": 2}
        processor = subject("b")
        result = processor.process(input)
        assert result == 2
