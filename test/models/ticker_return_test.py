from trade.models import TickerReturn


class TestTickerReturn:
    def test_table(self):
        assert TickerReturn._meta.table_name == "ticker_returns"

    def test_relations(self):
        assert "ticker" in TickerReturn._meta.fields
