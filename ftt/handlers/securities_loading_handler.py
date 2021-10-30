from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.securities_steps.securities_info_download_step import (
    SecuritiesInfoDownloadStep,
)
from ftt.handlers.securities_steps.securities_upsert_step import SecuritiesUpsertStep
from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from ftt.handlers.security_prices_steps.security_prices_upsert_step import (
    SecurityPricesUpsertStep,
)


class SecuritiesLoadingHandler(Handler):
    params = ("securities", "start_period", "end_period", "interval")

    handlers = [
        (SecuritiesInfoDownloadStep, "securities"),
        (SecuritiesUpsertStep, SecuritiesInfoDownloadStep.key),
        (
            SecurityPricesDownloadStep,
            SecuritiesUpsertStep.key,
            "start_period",
            "end_period",
            "interval",
        ),
        (SecurityPricesUpsertStep, SecurityPricesDownloadStep.key, "interval"),
        (ReturnResult, SecuritiesUpsertStep.key),
    ]
