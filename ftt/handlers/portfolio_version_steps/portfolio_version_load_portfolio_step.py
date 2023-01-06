from result import Result, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioVersionLoadPortfolioStep(AbstractStep):
    """
    Loads Portfolio from database by given portfolio version.

    Accepts
        portfolio_version: schemas.PortfolioVersion

    Returns
        portfolio: schemas.Portfolio
    """

    key = "portfolio"

    @classmethod
    def process(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[schemas.Portfolio, str]:
        find_by_portfolio_version = as_result(Exception)(
            PortfoliosRepository.find_by_portfolio_version
        )
        result = find_by_portfolio_version(portfolio_version)

        return result
