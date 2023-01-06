import pytest
from result import Ok

from ftt.storage import schemas
from ftt.ui.workers import PortfolioVersionOptimizationWorker


class TestPortfolioVersionOptimizationWorker:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionOptimizationWorker

    @pytest.mark.skip(reason="Have to mock threadpool.start")
    def test_emit_result(self, subject, mocker):
        result = Ok(1)
        context = mocker.patch(
            "ftt.ui.workers.PortfolioVersionOptimizationHandler",
        )
        context.return_value.handle.return_value = result

        success_callback = mocker.Mock()
        failure_callback = mocker.Mock()
        complete_callback = mocker.Mock()

        subject.perform(
            portfolio_version=schemas.PortfolioVersion(id=123),
            success_callback=success_callback,
            failure_callback=failure_callback,
            complete_callback=complete_callback,
        )

        success_callback.assert_called_once_with(result)
        complete_callback.assert_called_once_with()
        subject.signals.result.emit.assert_called_once_with(result)
