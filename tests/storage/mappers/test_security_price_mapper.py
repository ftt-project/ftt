import pandas as pd
import pytest

from ftt.storage.mappers.security_price_mapper import SecurityPriceMapper


class TestSecurityPriceMapper:
    @pytest.fixture
    def subject(self):
        return SecurityPriceMapper

    @pytest.fixture
    def dataframe(self):
        return pd.DataFrame(
            data={
                "Adj Close": [124.279999, 125.059998, 123.540001],
                "Close": [124.279999, 125.059998, 123.540001],
                "High": [125.349998, 125.239998, 124.849998],
                "Low": [123.940002, 124.050003, 123.129997],
                "Open": [125.080002, 124.279999, 124.680000],
                "Volume": [67637100, 59278900, 76229200],
            },
            index=pd.DatetimeIndex(
                ["2021-06-01 01:01:01", "2021-06-02 01:01:01", "2021-06-03 01:01:01"]
            ),
        ).rename_axis("Date")

    def test_from_dataframe_to_dict(self, subject, dataframe):
        collection = subject.from_dataframe(dataframe)
        assert len(collection) == 3

        result = collection.to_dicts()

        assert type(result) == list
        assert len(result) == 3
        assert type(result[0]) == dict
        assert list(result[0].keys()) == [
            "datetime",
            "adj_close",
            "close",
            "high",
            "low",
            "open",
            "volume",
        ]
