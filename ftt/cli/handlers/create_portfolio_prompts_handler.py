from ftt.cli.handlers.steps.portfolio_fields_prompts_step import (
    PortfolioFieldsPromptsStep,
)
from ftt.cli.handlers.steps.portfolio_version_fields_prompts_step import (
    PortfolioVersionFieldsPromptsStep,
)
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult


class CreatePortfolioPromptsHandler(Handler):
    params = ()

    handlers = [
        (PortfolioFieldsPromptsStep,),
        (PortfolioVersionFieldsPromptsStep,),
        (
            ReturnResult,
            PortfolioFieldsPromptsStep.key,
            PortfolioVersionFieldsPromptsStep.key,
        ),
    ]
