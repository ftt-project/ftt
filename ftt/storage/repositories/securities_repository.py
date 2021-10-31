from datetime import datetime
from typing import List, Tuple

from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.models.weight import Weight
from ftt.storage.repositories.repository import Repository


class SecuritiesRepository(Repository):
    @classmethod
    def get_by_name(cls, name: str) -> Security:
        return Security.get(Security.symbol == name)

    @classmethod
    def get_by_id(cls, id: int) -> Security:
        return Security.get_by_id(id)

    @classmethod
    def save(cls, record: Security) -> Security:
        record.updated_at = datetime.now()
        record.save()
        return record

    @classmethod
    def upsert(cls, data: dict) -> Tuple[Security, bool]:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        result = Security.get_or_create(
            symbol=data["symbol"], exchange=data["exchange"], defaults=data
        )
        return result

    @classmethod
    def exist(cls, name: str) -> int:
        count = Security.select().where(Security.symbol == name).count()
        return count > 0

    @classmethod
    def create(cls, data: dict) -> Security:
        raise NotImplementedError()

    @classmethod
    def find_securities(cls, portfolio_version: PortfolioVersion) -> List[Security]:
        result = (
            Security.select()
            .join(Weight)
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
        )
        return list(result)
