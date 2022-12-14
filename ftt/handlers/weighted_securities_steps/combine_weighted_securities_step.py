from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas


class CombineWeightedSecuritiesStep(AbstractStep):
    key = "combined_weighted_securities"

    @classmethod
    def process(
        cls,
        portfolio_weighted_securities: list[schemas.WeightedSecurity],
        portfolio_version_weighted_securities: list[schemas.WeightedSecurity],
    ) -> Result[list[schemas.WeightedSecurity], str]:
        portfolio_weighted_securities_set = {*portfolio_weighted_securities}
        portfolio_version_weighted_securities_set = {
            *portfolio_version_weighted_securities
        }
        merged = portfolio_version_weighted_securities_set.union(
            portfolio_weighted_securities_set
        )

        for weighted_security in merged:
            weighted_security.weighted = (
                weighted_security in portfolio_version_weighted_securities_set
            )
            weighted_security.discarded = (
                weighted_security not in portfolio_weighted_securities_set
            )

        return Ok([*merged])
