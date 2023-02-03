from datetime import datetime
from typing import Tuple

from playhouse.shortcuts import model_to_dict  # type: ignore

from ftt.storage import schemas
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
        from ftt.storage.models import Security

        security = Security.get_by_id(data.pop("security").id)
        result = SecurityPrice.get_or_create(
            security=security,
            datetime=data["datetime"],
            interval=data["interval"],
            defaults=data,
        )
        return result

    @staticmethod
    def create(self, data: dict) -> SecurityPrice:
        raise NotImplementedError()

    @staticmethod
    def save(self, model: SecurityPrice) -> SecurityPrice:
        raise NotImplementedError()

    @staticmethod
    def get_by_id(self, id: int) -> SecurityPrice:
        raise NotImplementedError()

    @staticmethod
    def security_price_time_vector(
        security: schemas.Security,
        interval: str,
        period_start: datetime,
        period_end: datetime,
    ) -> list[schemas.SecurityPrice]:
        records = (
            SecurityPrice.select()
            .where(
                SecurityPrice.security_id == security.id,
                SecurityPrice.interval == interval,
                (
                    (SecurityPrice.datetime >= period_start)
                    & (SecurityPrice.datetime <= period_end)
                ),
            )
            .order_by(SecurityPrice.datetime.asc())
        ).execute()
        records_as_dict = [
            {**model_to_dict(record), **{"symbol": security.symbol}}
            for record in records
        ]

        return [schemas.SecurityPrice(**record) for record in records_as_dict]
