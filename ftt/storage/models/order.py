import peewee

from ftt.storage.models.base import Base
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security


class Order(Base):
    security = peewee.ForeignKeyField(Security, backref="orders")
    type = peewee.CharField()
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="orders")
    status = peewee.CharField()
    executed_at = peewee.DateTimeField(null=True)
    desired_price = peewee.DecimalField(null=True)
    execution_size = peewee.IntegerField(null=True)
    execution_price = peewee.DecimalField(null=True)
    execution_value = peewee.DecimalField(null=True)
    execution_commission = peewee.DecimalField(null=True)

    Created = "Created"
    Submitted = "Submitted"
    Accepted = "Accepted"
    Partial = "Partial"
    Completed = "Completed"
    Canceled = "Canceled"
    Expired = "Expired"
    Margin = "Margin"
    Rejected = "Rejected"

    STATUSES = [
        "Created",
        "Submitted",
        "Accepted",
        "Partial",
        "Completed",
        "Canceled",
        "Expired",
        "Margin",
        "Rejected",
    ]

    NOT_CLOSED_STATUSES = [
        "Created",
        "Submitted",
        "Accepted",
    ]

    SUCCEED_STATUSES = ["Completed"]

    class Meta:
        table_name = "orders"
