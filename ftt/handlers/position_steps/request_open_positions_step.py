from result import Ok, Result

from ftt.brokers.position import Position
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep


class RequestOpenPositionsStep(AbstractStep):
    key = "open_positions"

    @classmethod
    def process(cls) -> Result[list[Position], str]:
        config = {"host": "127.0.0.1", "port": 7497, "client_id": 1234}
        brokerage_service = build_brokerage_service("Interactive Brokers", config)
        open_positions = brokerage_service.open_positions()

        return Ok(open_positions)
