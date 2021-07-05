from trade.storage.models.order import Order
from trade.storage.models.security import Security


class TestSecurity:
    def test_table(self):
        assert Security._meta.table_name == "securities"

    def test_relations(self):
        assert Security.orders.rel_model == Order
