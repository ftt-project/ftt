from result import Ok, Result

from ftt.brokers.position import Position
from ftt.handlers.handler.abstract_step import AbstractStep


class RequestOpenPositionsStep(AbstractStep):
    key = "open_positions"

    @classmethod
    def process(cls, brokerage_service) -> Result[list[Position], str]:
        open_positions = brokerage_service.open_positions()
        # TODO: handle when it returns None because of the broker connection
        # TODO handle when open_positions is None
        return Ok(open_positions or [])
