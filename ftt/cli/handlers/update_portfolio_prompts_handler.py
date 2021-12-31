from ftt.cli.handlers.steps.portfolio_version_fields_prompts_step import (
    PortfolioVersionFieldsPromptsStep,
)
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult


class UpdatePortfolioPromptsHandler(Handler):
    params = ("defaults",)

    handlers = [
        (PortfolioVersionFieldsPromptsStep, "defaults"),
        (ReturnResult, PortfolioVersionFieldsPromptsStep.key),
    ]
