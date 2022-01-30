from datetime import datetime
from typing import Tuple

from ftt.storage.models import Security
from ftt.storage.models.security_price import SecurityPrice
from ftt.storage.repositories.repository import Repository


class SecurityPricesRepository(Repository):
    @classmethod
    def upsert(cls, data: dict) -> Tuple[SecurityPrice, bool]:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        data["change"] = data["close"] - data["open"]
        data["percent_change"] = round(
            (data["close"] - data["open"]) / data["close"] * 100, 5
        )
        result = SecurityPrice.get_or_create(
            security=data["security"],
            datetime=data["datetime"],
            interval=data["interval"],
            defaults=data,
        )
        return result

    @staticmethod
    def create(self, data: dict) -> SecurityPrice:
        pass

    @staticmethod
    def save(self, model: SecurityPrice) -> SecurityPrice:
        pass

    @staticmethod
    def get_by_id(self, id: int) -> SecurityPrice:
        pass

    @staticmethod
    def find_by_security_prices(
        security: Security, interval: str, period_start: datetime, period_end: datetime
    ) -> list[SecurityPrice]:
        query = (
            SecurityPrice.select()
            .where(
                SecurityPrice.security == security,
                SecurityPrice.interval == interval,
                (
                    (SecurityPrice.datetime >= period_start)
                    & (SecurityPrice.datetime <= period_end)
                ),
            )
            .order_by(SecurityPrice.datetime.asc())
        )

        return query.execute()
