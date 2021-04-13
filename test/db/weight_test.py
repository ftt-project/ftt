from trade.db import Weight


class TestWeight:
    def test_table(self):
        assert Weight._meta.table_name == "weights"

    def test_relations(self):
        assert "ticker" in Weight._meta.fields
        assert "portfolio" in Weight._meta.fields
