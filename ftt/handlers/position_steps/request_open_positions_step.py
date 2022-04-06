from result import Ok, Result

from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.position import Position
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep


class RequestOpenPositionsStep(AbstractStep):
    key = "open_positions"

    @classmethod
    def process(cls) -> Result[list[Position], str]:
        brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig)
        open_positions = brokerage_service.open_positions()
        # TODO handle when open_positions is None
        return Ok(open_positions)
