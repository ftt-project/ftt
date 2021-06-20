from result import Ok, Err

from trade.storage.repositories import PortfoliosRepository


class PortfolioCreateStep:
    key = "portfolio"

    @classmethod
    def process(cls, **input):
        params = input[cls.key]
        result = PortfoliosRepository.create(**params)

        if result.id is not None:
            input[cls.key]["result"] = result
            return Ok(input)
        else:
            return Err(input)
