from collections import namedtuple
from datetime import datetime

import pytest

from trade.storage.models import Weight, Security, Portfolio


@pytest.fixture
def weights_seed(ticker_name="AA.BB", current_position=2, planned_position=10):
    Weight.delete().execute()
    Security.delete().execute()
    Portfolio.delete().execute()

    ticker = Security.create(
        ticker=ticker_name,
        exchange="TOR",
        exchange_name="TOR",
        type="stock",
        type_display="stock",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    portfolio = Portfolio.create(
        name="P1"
    )

    weight = Weight.create(
        portfolio=portfolio,
        ticker=ticker,
        position=current_position,
        planned_position=planned_position
    )

    return namedtuple("SeedData", ["ticker", "portfolio", "weight"])(
        ticker, portfolio, weight
    )
