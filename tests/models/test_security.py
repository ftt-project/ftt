from trade.storage.models import Security, Order


class TestSecurity:
    def test_table(self):
        assert Security._meta.table_name == "securities"

    def test_relations(self):
        assert Security.orders.rel_model == Order
