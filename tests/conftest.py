from datetime import datetime

import pytest
from pandas import DataFrame, DatetimeIndex

from ftt.storage import schemas, Storage
from ftt.storage.models import PortfolioSecurity
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.models.security_price import SecurityPrice
from ftt.storage.models.weight import Weight

from ftt.application import Application

Application.initialize(test_mode=True)


@pytest.fixture(autouse=True, scope="function")
def transactional():
    try:
        yield
    finally:
        for model in Storage.get_models():
            model.delete().execute()


@pytest.fixture(autouse=True, scope="session")
def db_reinitialize():
    try:
        yield
    finally:
        sm = Storage.storage_manager()
        sm.drop_tables(Storage.get_models())


@pytest.fixture
def data_security():
    return {
        "symbol": "AA.XX",
        "exchange": "SYD",
        "company_name": "Company AAXX",
        "exchange_name": "SYD",
        "quote_type": "Stock",
        "type_display": "Stock",
        "industry": "Technologies",
        "sector": "Technology",
        "country": "US",
        "short_name": "Short name",
        "long_name": "Long name",
        "currency": "USD",
    }


@pytest.fixture
def schema_security(data_security):
    return schemas.Security(**data_security)


@pytest.fixture
def security(data_security):
    security = Security.create(
        **(data_security | {"created_at": datetime.now(), "updated_at": datetime.now()})
    )
    try:
        yield security
    finally:
        security.delete_instance()


@pytest.fixture
def security_factory():
    def _security(symbol="AA.XX"):
        return Security.create(
            symbol=symbol,
            exchange="SYD",
            company_name="Company AAXX",
            exchange_name="SYD",
            quote_type="Stock",
            type_display="Stock",
            industry="Technologies",
            sector="Technology",
            country="US",
            short_name="Short name",
            long_name="Long name",
            currency="USD",
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _security

    Security.delete().execute()


@pytest.fixture
def security_price(security):
    price = SecurityPrice.create(
        security=security,
        datetime=datetime.today(),
        open=100,
        high=110,
        low=90,
        close=101,
        volume=1000000,
        interval="5m",
        change=1,
        percent_change=1,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield price
    finally:
        price.delete_instance()


@pytest.fixture
def security_price_factory():
    def _security_price(
        security,
        dt=None,
        open=100,
        high=110,
        low=90,
        close=100,
        volume=1000,
        interval="5m",
    ):
        return SecurityPrice.create(
            security=security,
            datetime=dt if dt is not None else datetime.today(),
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
            interval=interval,
            change=1,
            percent_change=1,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _security_price

    SecurityPrice.delete().execute()


@pytest.fixture
def data_portfolio():
    return {
        "name": "Test portfolio",
        "description": "Test portfolio description",
        "period_start": datetime.now(),
        "period_end": datetime.now(),
        "value": 1000.50,
        "interval": "5m",
        "securities": [],
    }


@pytest.fixture
def schema_portfolio(data_portfolio):
    return schemas.Portfolio(**data_portfolio)


@pytest.fixture
def portfolio(data_portfolio):
    portfolio = Portfolio.create(
        name=data_portfolio["name"],
        description=data_portfolio["description"],
        period_start=data_portfolio["period_start"],
        period_end=data_portfolio["period_end"],
        value=data_portfolio["value"],
        interval=data_portfolio["interval"],
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield portfolio
    finally:
        portfolio.delete_instance()


@pytest.fixture
def portfolio_factory():
    def _portfolio(name):
        return Portfolio.create(
            name=name,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _portfolio

    Portfolio.delete().execute()


@pytest.fixture
def portfolio_security(portfolio, security) -> PortfolioSecurity:
    portfolio_security = PortfolioSecurity.create(
        portfolio=portfolio,
        security=security,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield portfolio_security
    finally:
        portfolio_security.delete_instance()


@pytest.fixture
def portfolio_security_factory():
    def _portfolio_security_factory(portfolio, security):
        return PortfolioSecurity.create(
            portfolio=portfolio,
            security=security,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _portfolio_security_factory

    SecurityPrice.delete().execute()


@pytest.fixture
def data_portfolio_version(portfolio):
    return {
        "portfolio": portfolio,
        "version": 1,
        "active": True,
        "optimization_strategy_name": "Test strategy",
        "allocation_strategy_name": "Test allocation strategy",
        "expected_annual_return": None,
        "annual_volatility": None,
        "sharpe_ratio": None,
    }


@pytest.fixture
def schema_portfolio_version(data_portfolio_version):
    return schemas.PortfolioVersion(**data_portfolio_version)


@pytest.fixture
def portfolio_version(portfolio, data_portfolio_version):
    portfolio_version = PortfolioVersion.create(
        portfolio=portfolio,
        version=data_portfolio_version["version"],
        active=data_portfolio_version["active"],
        optimization_strategy_name=data_portfolio_version["optimization_strategy_name"],
        expected_annual_return=data_portfolio_version["expected_annual_return"],
        annual_volatility=data_portfolio_version["annual_volatility"],
        sharpe_ratio=data_portfolio_version["sharpe_ratio"],
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield portfolio_version
    finally:
        portfolio_version.delete_instance()


@pytest.fixture
def portfolio_version_factory(portfolio):
    def _portfolio_version(
        value=30000.0,
        portfolio=portfolio,
        version=1,
        optimization_strategy_name="historical",
        allocation_strategy_name="default",
    ):
        return PortfolioVersion.create(
            portfolio=portfolio,
            version=version,
            value=value,
            optimization_strategy_name=optimization_strategy_name,
            allocation_strategy_name=allocation_strategy_name,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _portfolio_version

    PortfolioVersion.delete().execute()


@pytest.fixture
def weight(portfolio_version, security):
    weight = Weight.create(
        portfolio_version=portfolio_version,
        security=security,
        planned_position=10,
        position=2,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield weight
    finally:
        weight.delete_instance()


@pytest.fixture
def weight_factory():
    def _weight(portfolio_version, security, planned_position=0, position=0):
        return Weight.create(
            portfolio_version=portfolio_version,
            security=security,
            planned_position=planned_position,
            position=position,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    yield _weight

    Weight.delete().execute()


@pytest.fixture
def weighted_security_factory():
    def _weighted_security_factory(
        security,
        portfolio_version,
        portfolio,
        position=0,
        planned_position=100,
        amount=0,
    ):
        return schemas.WeightedSecurity(
            symbol=security.symbol,
            portfolio=schemas.Portfolio.from_orm(portfolio),
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version),
            security=schemas.Security.from_orm(security),
            position=position,
            planned_position=planned_position,
            amount=amount,
        )

    yield _weighted_security_factory


@pytest.fixture
def order(security, portfolio_version, portfolio, weight):
    order = Order.create(
        security=security,
        action="BUY",
        portfolio=portfolio,
        portfolio_version=portfolio_version,
        weight=weight,
        status="Created",
        order_type="MKT",
        desired_price=100,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield order
    finally:
        order.delete_instance()


@pytest.fixture
def mock_external_info_requests(mocker):
    mock = mocker.patch("yfinance.Ticker")
    mock.return_value.info = {
        "symbol": "AAPL",
        "exchange": "NMS",
        "sector": "Technology",
        "country": "Canada",
        "industry": "Software—Application",
        "currency": "USD",
        "quoteType": "stock",
        "shortName": "Apple Inc.",
        "longName": "Apple Inc.",
    }

    return mock


@pytest.fixture
def mock_external_historic_data_requests(mocker):
    mocker.patch("yfinance.pdr_override")
    mock = mocker.patch("pandas_datareader.data.get_data_yahoo")
    mock.return_value = DataFrame(
        data={
            "Adj Close": [124.279999, 125.059998, 123.540001],
            "Close": [124.279999, 125.059998, 123.540001],
            "High": [125.349998, 125.239998, 124.849998],
            "Low": [123.940002, 124.050003, 123.129997],
            "Open": [125.080002, 124.279999, 124.680000],
            "Volume": [67637100, 59278900, 76229200],
        },
        index=DatetimeIndex(
            [
                "2021-06-01 01:01:01",
                "2021-06-02 01:01:01",
                "2021-06-03 01:01:01",
            ]
        ),
    ).rename_axis("Date")

    return mock


@pytest.fixture
def securities_weights_list_factory(
    security_factory, weight_factory, security_price_factory
):
    def _securities_weights_list(portfolio_version, date_range, interval, n=11):
        fixture_data = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

        weights = []
        for i, symbol in enumerate(fixture_data[:n]):
            security = security_factory(symbol=symbol)
            for dt in date_range:
                _ = security_price_factory(
                    security=security,
                    dt=dt.to_pydatetime(),
                    interval=interval,
                    close=dt.day,
                )
            weight = weight_factory(
                security=security, portfolio_version=portfolio_version
            )
            weights.append(weight)

        return weights

    yield _securities_weights_list
