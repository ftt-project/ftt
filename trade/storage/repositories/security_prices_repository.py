from datetime import datetime
from typing import List, Tuple

from trade.storage.models import SecurityPrice
from trade.storage.repositories.repository_interface import RepositoryInterface


class SecurityPricesRepository(RepositoryInterface):
    @classmethod
    def upsert(cls, data: List[dict]) -> Tuple[SecurityPrice, bool]:
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
