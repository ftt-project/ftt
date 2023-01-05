import pytest

from ftt.storage import schemas
from ftt.storage.repositories.portfolio_security_repository import (
    PortfolioSecurityRepository,
)


class TestPortfolioSecurityRepository:
    @pytest.fixture
    def subject(self):
        return PortfolioSecurityRepository

    def test_associate(self, subject, portfolio, security):
        result = subject.associate(
            schemas.Portfolio.from_orm(portfolio), schemas.Security.from_orm(security)
        )

        assert type(result) == schemas.PortfolioSecurity
        assert result.id is not None
        assert result.portfolio.id == portfolio.id
        assert result.security.id == security.id

    def test_list(self, subject, portfolio, security):
        subject.associate(
            schemas.Portfolio.from_orm(portfolio), schemas.Security.from_orm(security)
        )

        result = subject.list(schemas.Portfolio.from_orm(portfolio))

        assert type(result) == list
        assert len(result) == 1
        assert result[0].id is not None
        assert result[0].portfolio.id == portfolio.id
        assert result[0].security.id == security.id