import pandas as pd
import pytest


@pytest.fixture
def prices_list_factory():
    def _prices_list_factory(len=5):
        securities = ["A", "B", "C", "D", "E"][:len]
        index = pd.date_range(start="2020.01.01", end="2020.12.31")
        return pd.DataFrame(
            data={**{s: [i.day for i in index.to_series()] for s in securities}},
            index=index,
        )

    yield _prices_list_factory
