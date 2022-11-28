from datetime import datetime

from ftt.storage import schemas, models
from ftt.storage.models.portfolio_security import PortfolioSecurity
from ftt.storage.repositories.repository import Repository


class PortfolioSecurityRepository(Repository):
    @classmethod
    def associate(
        cls, portfolio: schemas.Portfolio, security: schemas.Security
    ) -> schemas.PortfolioSecurity:
        portfolio_model = models.Portfolio.get_by_id(portfolio.id)
        security_model = models.Security.get_by_id(security.id)
        result, created = PortfolioSecurity.get_or_create(
            portfolio=portfolio_model,
            security=security_model,
            defaults={"updated_at": datetime.now(), "created_at": datetime.now()},
        )
        return schemas.PortfolioSecurity.from_orm(result)

    # @classmethod
    # def get_by_portfolio_id(cls, portfolio_id: int) -> list[schemas.Security]:
    #     result = (
    #         Security.select()
    #         .join(PortfolioSecurity)
    #         .join(Portfolio)
    #         .where(Portfolio.id == portfolio_id)
    #     )
    #     return list(result)
    #
    # @classmethod
    # def get_by_security_id(cls, security_id: int) -> list[schemas.Portfolio]:
    #     result = (
    #         Portfolio.select()
    #         .join(PortfolioSecurity)
    #         .join(Security)
    #         .where(Security.id == security_id)
    #     )
    #     return list(result)
    #
    # @classmethod
    # def get_by_portfolio_id_and_security_id(
    #     cls, portfolio_id: int, security_id: int
    # ) -> schemas.PortfolioSecurity | None:
    #     try:
    #         result = PortfolioSecurity.get(
    #             PortfolioSecurity.portfolio == portfolio_id,
    #             PortfolioSecurity.security == security_id,
    #         )
    #     except PortfolioSecurity.DoesNotExist:
    #         return None
    #
    #     return result
    #
    # @classmethod
    # def get_by_portfolio_id_and_security_symbol(
    #     cls, portfolio_id: int, security_symbol: str
    # ) -> schemas.PortfolioSecurity | None:
    #     try:
    #         result = PortfolioSecurity.get(
    #             PortfolioSecurity.portfolio == portfolio_id,
    #             Security.symbol == security_symbol,
    #         )
    #     except PortfolioSecurity.DoesNotExist:
    #         return None
    #
    #     return result
    #
    # @classmethod
    # def get_by_portfolio_id_and_security_symbols(
    #     cls, portfolio_id: int, security_symbols: list[str]
    # ) -> list[schemas.PortfolioSecurity]:
    #     result = (
    #         PortfolioSecurity.select()
    #         .join(Security)
    #         .where(
    #             PortfolioSecurity.portfolio == portfolio_id,
    #             Security.symbol.in_(security_symbols),
    #         )
    #     )
    #     return list(result)
    #
    # @classmethod
    # def get_by_portfolio_id_and_security_symbols_and_exchange(
    #     cls, portfolio_id: int, security_symbols: list[str], exchange: str
    # ) -> list[schemas.PortfolioSecurity]:
    #     result = (
    #         PortfolioSecurity.select()
    #         .join(Security)
    #         .where(
    #             PortfolioSecurity.portfolio == portfolio_id,
    #             Security.symbol.in_(security_symbols),
    #             Security.exchange == exchange,
