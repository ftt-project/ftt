import pandas as pd
import pytest

from ftt.handlers.weights_steps.weights_calculate_step import (
    WeightsCalculateStep,
    WeightsCalculateStepResult,
)


class TestWeightsCalculateStep:
    @pytest.fixture
    def subject(self):
        return WeightsCalculateStep

    @pytest.fixture()
    def dataframes(self):
        return pd.DataFrame(
            data={
                "AA.XX": [124.279999, 125.059998, 123.540001],
                "AA.YY": [125.080002, 124.279999, 124.680000],
            },
            index=pd.DatetimeIndex(
                ["2021-06-01 01:01:01", "2021-06-02 01:01:01", "2021-06-03 01:01:01"]
            ),
        ).rename_axis("datetime")

    def test_calculates_weights(
        self, subject, dataframes, portfolio, portfolio_version
    ):
        result = subject.process(dataframes, portfolio, portfolio_version)

        assert result.is_ok()
        assert type(result.value) == WeightsCalculateStepResult
        assert result.value.allocation["AA.YY"] == 240
        assert result.value.leftover == 76.79999999999927
