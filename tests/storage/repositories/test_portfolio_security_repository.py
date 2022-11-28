import pytest

from ftt.storage import schemas
from ftt.storage.repositories.portfolio_security_repository import PortfolioSecurityRepository


class TestPortfolioSecurityRepository:
    @pytest.fixture
    def subject(self):
        return PortfolioSecurityRepository

    def test_associate(self, subject, portfolio, security):
        result = subject.associate(schemas.Portfolio.from_orm(portfolio), schemas.Security.from_orm(security))

        assert type(result) == schemas.PortfolioSecurity
        assert result.id is not None
        assert result.portfolio.id == portfolio.id
        assert result.security.id == security.id
