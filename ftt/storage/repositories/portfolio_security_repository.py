from datetime import datetime

from ftt.storage import schemas, models
from ftt.storage.models.portfolio_security import PortfolioSecurity
from ftt.storage.repositories.repository import Repository


class PortfolioSecurityRepository(Repository):
    @classmethod
    def associate(
        cls, portfolio: schemas.Portfolio, security: schemas.Security
    ) -> schemas.PortfolioSecurity:
        portfolio_record = models.Portfolio.get_by_id(portfolio.id)
        security_record = models.Security.get_by_id(security.id)
        result, created = PortfolioSecurity.get_or_create(
            portfolio=portfolio_record,
            security=security_record,
            defaults={"updated_at": datetime.now(), "created_at": datetime.now()},
        )
        return schemas.PortfolioSecurity.from_orm(result)
