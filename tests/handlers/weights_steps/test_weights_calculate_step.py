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
                "AA.XX": [
                    65.651581,
                    65.555298,
                    65.564934,
                    63.649014,
                    63.610493,
                    63.206135,
                    62.522568,
                    62.647720,
                    63.321663,
                    63.379436,
                    63.157993,
                    62.599579,
                    62.763256,
                    62.435909,
                    62.464798,
                    62.127823,
                    62.936562,
                    62.984699,
                    62.243359,
                    61.492393,
                    61.704201,
                    61.983406,
                    63.283154,
                ],
                "AA.YY": [
                    100.968216,
                    100.496216,
                    100.216881,
                    100.265030,
                    101.632858,
                    103.270386,
                    103.048843,
                    103.752007,
                    105.283585,
                    104.975342,
                    105.476234,
                    106.738098,
                    107.181190,
                    106.805519,
                    108.173347,
                    105.328293,
                    106.357216,
                    106.910492,
                    107.376427,
                    107.026985,
                    107.376427,
                    108.453880,
                    108.745079,
                ],
            },
            index=pd.DatetimeIndex(
                [
                    "2021-10-08",
                    "2021-10-11",
                    "2021-10-12",
                    "2021-10-13",
                    "2021-10-14",
                    "2021-10-15",
                    "2021-10-18",
                    "2021-10-19",
                    "2021-10-20",
                    "2021-10-21",
                    "2021-10-22",
                    "2021-10-25",
                    "2021-10-26",
                    "2021-10-27",
                    "2021-10-28",
                    "2021-10-29",
                    "2021-11-01",
                    "2021-11-02",
                    "2021-11-03",
                    "2021-11-04",
                    "2021-11-05",
                    "2021-11-06",
                    "2021-11-07",
                ]
            ),
        ).rename_axis("datetime")

    def test_calculates_weights(
        self, subject, dataframes, portfolio, portfolio_version
    ):
        result = subject.process(dataframes, portfolio_version)

        assert result.is_ok()
        assert type(result.value) == WeightsCalculateStepResult
        assert result.value.allocation["AA.YY"] == 128
        assert result.value.leftover == 6.708755888197629
