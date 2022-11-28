from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.portfolio_security_repository import (
    PortfolioSecurityRepository,
)
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesAssociateWithPortfolioStep(AbstractStep):
    key = "portfolio_securities_collection"
    """
    Associate securities with portfolio through HBTM model portfolio securities.
    """

    @classmethod
    def process(
        cls, portfolio: schemas.Portfolio, securities: list[schemas.Security]
    ) -> Result[list[schemas.Security], str]:
        associated_securities: list[schemas.Security] = []
        for security in securities:
            security: schemas.Security = SecuritiesRepository.get_by_name(
                security.symbol
            )
            result: schemas.PortfolioSecurity = PortfolioSecurityRepository.associate(
                portfolio, security
            )
            associated_securities.append(result.security)

        return Ok(associated_securities)
