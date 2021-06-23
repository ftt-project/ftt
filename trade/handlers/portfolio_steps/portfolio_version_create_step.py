from result import Ok, Err

from trade.storage.repositories import PortfolioVersionsRepository


class PortfolioVersionCreateStep:
    key = "portfolio_version"

    @classmethod
    def process(cls, version, portfolio):
        result = PortfolioVersionsRepository.create(
            version=version,
            portfolio_id=portfolio.id
        )
        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
