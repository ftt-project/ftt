from ftt.storage.models.security_price import SecurityPrice


class TestSecurityPrice:
    def test_table(self):
        assert SecurityPrice._meta.table_name == "security_prices"

    def test_relations(self):
        assert "security" in SecurityPrice._meta.fields
