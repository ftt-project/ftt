from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from ftt.storage import schemas


class SecuritiesInformationLoadingHandler(Handler):
    """
    Handler for loading securities information from yahoo finance and stores it locally
    """

    params = {"securities": list[schemas.Security]}

    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (SecuritiesUpsertStep, SecuritiesInfoDownloadStep.key),
        (ReturnResult, SecuritiesUpsertStep.key),
    ]
