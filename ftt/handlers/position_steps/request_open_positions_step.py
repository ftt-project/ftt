from result import Ok, Result

from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.position import Position
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.logger import Logger


class RequestOpenPositionsStep(AbstractStep):
    key = "open_positions"

    @classmethod
    def process(cls, brokerage_service) -> Result[list[Position], str]:
        open_positions = brokerage_service.open_positions()
        # TODO handle when open_positions is None
        print("open_positions", open_positions)
        return Ok(open_positions or [])
