from enum import Enum

import peewee

from ftt.storage.models.base import Base
from ftt.storage.models import Portfolio, Weight
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security


class Order(Base):
    security = peewee.ForeignKeyField(Security, backref="orders")
    action = peewee.CharField()
    order_type = peewee.CharField()
    portfolio = peewee.ForeignKeyField(Portfolio, backref="orders")
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="orders")
    weight = peewee.ForeignKeyField(Weight, backref="weight")
    status = peewee.CharField()
    external_id = peewee.CharField(null=True)
    executed_at = peewee.DateTimeField(null=True)
    desired_size = peewee.DecimalField(null=True)
    desired_price = peewee.DecimalField(null=True)
    execution_size = peewee.IntegerField(null=True)
    execution_price = peewee.DecimalField(null=True)
    execution_value = peewee.DecimalField(null=True)
    execution_commission = peewee.DecimalField(null=True)

    # Move from here to a separate class as it creates additional imports when it is not necessary
    class Status(str, Enum):
        CREATED = "Created"
        SUBMITTED = "Submitted"
        ACCEPTED = "Accepted"
        PARTIAL = "Partial"
        COMPLETED = "Completed"
        CANCELED = "Canceled"
        EXPIRED = "Expired"
        MARGIN = "Margin"
        REJECTED = "Rejected"

    class NotClosedStatus(str, Enum):
        CREATED = "Created"
        SUBMITTED = "Submitted"
        ACCEPTED = "Accepted"

    class SucceedStatus(str, Enum):
        COMPLETED = "Completed"
        PARTIAL = "Partial"

    class Meta:
        table_name = "orders"
