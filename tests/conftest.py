from datetime import datetime

import pytest
from pandas import DataFrame, DatetimeIndex

from ftt.storage import Storage
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
    connection = Storage.get_database()
    with connection.atomic() as transaction:
        try:
            yield
        finally:
            transaction.rollback()


@pytest.fixture
def security():
    security = Security.create(
        symbol="AA.XX",
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
def portfolio():
    portfolio = Portfolio.create(
        name="Portfolio TEST 1",
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
def portfolio_version(portfolio):
    portfolio_version = PortfolioVersion.create(
        portfolio=portfolio,
        version=1,
        value=30000.0,
        period_start=datetime(2020, 1, 1),
        period_end=datetime(2020, 10, 5),
        interval="1mo",
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
        interval="1mo",
        period_start=datetime(2020, 1, 1),
        period_end=datetime(2020, 10, 5),
    ):
        return PortfolioVersion.create(
            portfolio=portfolio,
            version=version,
            value=value,
            period_start=period_start,
            period_end=period_end,
            interval=interval,
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
def order(security, portfolio_version, portfolio, weight):
    order = Order.create(
        security=security,
        action="BUY",
        portfolio=portfolio,
        portfolio_version=portfolio_version,
        weight=weight,
        status="Created",
        order_type="MARKET",
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
