from datetime import datetime
from typing import List, Tuple

from ftt.storage import schemas, models
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.models.weight import Weight
from ftt.storage.repositories.repository import Repository


class SecuritiesRepository(Repository):
    @classmethod
    def get_by_name(cls, name: str) -> schemas.Security | None:
        try:
            model = Security.get(Security.symbol == name)
        except Security.DoesNotExist:
            return None

        return schemas.Security.from_orm(model)

    @classmethod
    def get_by_id(cls, id: int) -> Security:
        return Security.get_by_id(id)

    @classmethod
    def save(cls, record: Security) -> Security:
        record.updated_at = datetime.now()
        record.save()
        return record

    @classmethod
    def upsert(cls, schema_model: schemas.Security) -> Tuple[schemas.Security, bool]:
        data = schema_model.dict()
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        result = Security.get_or_create(
            symbol=data["symbol"], exchange=data["exchange"], defaults=data
        )
        return schemas.Security.from_orm(result[0]), result[1]

    @classmethod
    def exist(cls, name: str) -> int:
        count = Security.select().where(Security.symbol == name).count()
        return count > 0

    @classmethod
    def create(cls, data: dict) -> Security:
        raise NotImplementedError()

    @classmethod
    def find_securities(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> List[Security]:
        """
        TODO: Deprecated in favor of find_by_portfolio
        """
        result = (
            Security.select()
            .join(Weight)
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
        )
        return list(result)

    @classmethod
    def find_by_portfolio(cls, portfolio: schemas.Portfolio) -> list[schemas.Security]:
        portfolio_record = models.Portfolio.get(portfolio.id)

        result = (
            Security.select()
            .join(models.PortfolioSecurity)
            .join(models.Portfolio)
            .where(models.Portfolio.id == portfolio_record.id)
        )
        return [schemas.Security.from_orm(record) for record in result]
