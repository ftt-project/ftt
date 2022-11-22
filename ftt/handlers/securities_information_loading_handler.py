from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.securities_steps.securities_info_download_step import SecuritiesInfoDownloadStep


class SecuritiesInformationLoadingHandler(Handler):
    params = ("securities",)

    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (ReturnResult, SecuritiesInfoDownloadStep.key),
    ]