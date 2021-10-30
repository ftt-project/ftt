from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_config_file_reader import (
    PortfolioConfigFileReaderStep,
)
from ftt.handlers.portfolio_steps.portfolio_config_parser_step import (
    PortfolioConfigParserStep,
)


class PortfolioConfigHandler(Handler):
    params = ("path",)

    handlers = [
        (PortfolioConfigFileReaderStep, "path"),
        (PortfolioConfigParserStep, PortfolioConfigFileReaderStep.key),
        (ReturnResult, PortfolioConfigParserStep.key),
    ]
