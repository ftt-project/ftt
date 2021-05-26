import peewee

from trade.models import Base, Ticker, PortfolioVersion


class Order(Base):
    ticker = peewee.ForeignKeyField(Ticker, backref="orders")
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

    class Meta:
        table_name = "orders"
