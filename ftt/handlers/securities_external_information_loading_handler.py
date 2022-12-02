from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.storage import schemas


class SecuritiesExternalInformationLoadingHandler(Handler):
    """
    Handler for loading securities information from yahoo finance
    """

    params = {"securities": list[schemas.Security]}

    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (ReturnResult, SecuritiesInfoDownloadStep.key),
    ]
