from result import Ok, Err

from trade.storage.repositories import PortfoliosRepository


class PortfolioCreateStep:
    key = "portfolio"

    @classmethod
    def process(cls, name, amount):
        result = PortfoliosRepository.create(
            name=name,
            amount=amount
        )

        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
