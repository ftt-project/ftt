from ftt.cli.handlers.define_example_config_path_step import DefineExampleConfigPathStep
from ftt.cli.handlers.steps.define_package_path_step import DefinePackagePathStep
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_config_file_reader import (
    PortfolioConfigFileReaderStep,
)
from ftt.handlers.portfolio_steps.portfolio_config_parser_step import (
    PortfolioConfigParserStep,
)


class PortfolioConfigHandler(Handler):
    params = ()

    handlers = [
        (DefinePackagePathStep,),
        (DefineExampleConfigPathStep, DefinePackagePathStep.key),
        (PortfolioConfigFileReaderStep, DefineExampleConfigPathStep.key),
        (PortfolioConfigParserStep, PortfolioConfigFileReaderStep.key),
        (ReturnResult, PortfolioConfigParserStep.key),
    ]
