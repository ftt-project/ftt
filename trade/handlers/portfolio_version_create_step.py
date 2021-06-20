from result import Ok, Err

from trade.storage.repositories import PortfolioVersionsRepository


class PortfolioVersionCreateStep:
    key = "portfolio_version"

    @classmethod
    def process(cls, **input):
        params = input[cls.key]
        portfolio = input["portfolio"]["result"]
        result = PortfolioVersionsRepository.create(
            version=params["version"],
            portfolio_id=portfolio.id
        )
        if result.id is not None:
            input[cls.key]["result"] = result
            return Ok(input)
        else:
            return Err(input)
