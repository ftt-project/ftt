from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_config_file_reader import (
    PortfolioConfigFileReaderStep,
)
from trade.handlers.portfolio_steps.portfolio_config_parser_step import (
    PortfolioConfigParserStep,
)


class PortfolioConfigHandler(Handler):
    handlers = [
        (PortfolioConfigFileReaderStep, "path"),
        (PortfolioConfigParserStep, PortfolioConfigFileReaderStep.key),
        ReturnResult(PortfolioConfigParserStep.key),
    ]
